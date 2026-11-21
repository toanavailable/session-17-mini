"""Security Log Analyzer - Hệ thống phân tích nhật ký bảo mật."""

# =====================================================================
# BIẾN TOÀN CỤC
# =====================================================================
raw_logs = []           # Danh sách log đã làm sạch
processed_logs = []     # Danh sách log cảnh báo mức độ cao (ERROR / CRITICAL)

SPECIAL_CHARS = "!@#$"                                # Ký tự rác cần loại bỏ
CLEAN_TABLE = str.maketrans("", "", SPECIAL_CHARS)    # Bảng ánh xạ: xóa các ký tự trên
ALERT_KEYWORDS = ["ERROR", "CRITICAL"]


def clean_raw_logs(raw_text):
    """Làm sạch chuỗi log thô và tách thành danh sách.

    Tham số:
        raw_text (str): chuỗi log thô, nhiều log cách nhau bởi dấu ";"
    Trả về:
        list[str]: các dòng log đã bỏ ký tự đặc biệt (!@#$) và khoảng trắng thừa
    """
    cleaned_text = raw_text.translate(CLEAN_TABLE)      # xóa toàn bộ ký tự rác trong 1 lần quét
    return [" ".join(line.split()) for line in cleaned_text.split(";") if line.strip() != ""]


def filter_alert_logs(logs):
    """Lọc các log cảnh báo nguy hiểm (không phân biệt hoa thường).

    Tham số:
        logs (list[str]): danh sách log đã làm sạch
    Trả về:
        list[str]: các log chứa từ khóa ERROR hoặc CRITICAL
    """
    return [log for log in logs if any(keyword in log.upper() for keyword in ALERT_KEYWORDS)]


def is_ip_address(word):
    """Kiểm tra một từ có phải địa chỉ IPv4 hay không.

    Tham số:
        word (str): một từ trong dòng log
    Trả về:
        bool: True nếu gồm 4 phần số (0-255) ngăn cách bởi dấu chấm
    """
    parts = word.split(".")
    return len(parts) == 4 and all(part.isdigit() and int(part) <= 255 for part in parts)


def mask_ip(ip_address):
    """Che giấu 2 dải số cuối của IP. Ví dụ "192.168.1.1" -> "192.168.*.*".

    Tham số:
        ip_address (str): địa chỉ IP hợp lệ
    Trả về:
        str: địa chỉ IP đã che
    """
    parts = ip_address.split(".")
    return ".".join(parts[:2] + ["*", "*"])


def mask_ip_logs(logs):
    """Mã hóa địa chỉ IP trong từng dòng log; dòng không có IP được giữ nguyên.

    Tham số:
        logs (list[str]): danh sách log cảnh báo
    Trả về:
        list[str]: danh sách log mới đã che IP (không sửa list gốc)
    """
    return [" ".join(mask_ip(word) if is_ip_address(word) else word for word in log.split())
            for log in logs]


def main():
    """Vòng lặp menu chính."""
    global processed_logs
    while True:
        print("\n============ SECURITY LOG ANALYZER ============")
        print("1. Nhập và làm sạch dữ liệu Log thô")
        print("2. Lọc các Log cảnh báo mức độ cao (ERROR/CRITICAL)")
        print("3. Mã hóa địa chỉ IP (Masking)")
        print("4. Đóng hệ thống")
        print("=" * 47)
        choice = input("Chọn chức năng (1-4): ").strip()

        if choice == "1":
            print("--- NẠP DỮ LIỆU LOG ---")
            new_logs = clean_raw_logs(input("Nhập chuỗi log thô (cách nhau bởi dấu ;): "))
            if len(new_logs) == 0:
                print("Không có dòng log hợp lệ nào được nhập.")
            else:
                raw_logs.extend(new_logs)          # sửa trực tiếp list toàn cục
                print(f"Đã làm sạch và lưu {len(new_logs)} dòng log vào hệ thống.")

        elif choice == "2":
            print("--- LỌC CẢNH BÁO ---")
            if len(raw_logs) == 0:                                            # Bẫy 1
                print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.")
                continue
            processed_logs = filter_alert_logs(raw_logs)
            if len(processed_logs) == 0:
                print("Không tìm thấy cảnh báo nguy hiểm nào.")
            else:
                print(f"Tìm thấy {len(processed_logs)} cảnh báo nguy hiểm:")
                for log in processed_logs:
                    print(f"- {log}")

        elif choice == "3":
            print("--- MÃ HÓA IP ---")
            if len(raw_logs) == 0:                                            # Bẫy 1
                print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.")
                continue
            if len(processed_logs) == 0:
                print("Chưa có log cảnh báo nào để mã hóa, vui lòng thực hiện chức năng 2.")
                continue
            print("Báo cáo log an toàn:")
            for stt, log in enumerate(mask_ip_logs(processed_logs), start=1):
                print(f"{stt}. {log}")

        elif choice == "4":
            print("Đã đóng hệ thống Security Log Analyzer. Tạm biệt!")
            break

        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!")


if __name__ == "__main__":
    main()
