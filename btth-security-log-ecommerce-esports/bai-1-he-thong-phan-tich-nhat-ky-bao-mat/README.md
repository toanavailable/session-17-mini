# Bài 1 - Hệ thống phân tích nhật ký bảo mật (Security Log Analyzer)

## Đề bài

Hệ thống máy chủ bị tấn công DDoS và Spam, nhật ký hệ thống (System Logs) đổ về rất lớn: chuỗi văn bản lộn xộn chứa ký tự rác, địa chỉ IP và mã lỗi. Xử lý bằng vòng lặp `for` thông thường để cắt ghép chuỗi rất chậm và rườm rà. Cần dùng các phương thức xử lý chuỗi nâng cao (`split`, `join`, `replace`, `translate`, `maketrans`) kết hợp **List Comprehension** để làm sạch dữ liệu, che giấu (masking) IP nhạy cảm và trích xuất các cảnh báo quan trọng. Hai biến toàn cục: `raw_logs = []`, `processed_logs = []`.

### Menu

```
============ SECURITY LOG ANALYZER ============
1. Nhập và làm sạch dữ liệu Log thô
2. Lọc các Log cảnh báo mức độ cao (ERROR/CRITICAL)
3. Mã hóa địa chỉ IP (Masking)
4. Đóng hệ thống
===============================================
Chọn chức năng (1-4):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Nạp và làm sạch log | `clean_raw_logs(raw_text)` | `str.maketrans()` + `str.translate()` loại bỏ `!@#$`; `split(";")` tách nhiều log; lưu vào `raw_logs` |
| 2. Lọc cảnh báo | `filter_alert_logs(logs)` | **List Comprehension** giữ dòng chứa `ERROR` hoặc `CRITICAL` (không phân biệt hoa thường) → `processed_logs` |
| 3. Mã hóa IP | `mask_ip_logs(logs)` | `split()` tách từ, tìm chuỗi định dạng IP, đổi `192.168.1.1` → `192.168.*.*`, `join()` lại; **return** danh sách đã mã hóa |
| 4. Đóng hệ thống | `main()` | In thông báo kết thúc và thoát |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 | Gọi chức năng 2, 3 khi `raw_logs` trống | "Chưa có dữ liệu log, vui lòng thực hiện chức năng 1." |
| Bẫy 2 | Dòng log không chứa IP | Hàm mã hóa giữ nguyên dòng đó, không crash |

## (1) Phân tích và thiết kế

### Cơ chế `str.maketrans()` + `str.translate()`

`str.maketrans("", "", "!@#$")` tạo một **bảng ánh xạ (mapping table)** dạng dict, với khóa là **mã Unicode** của từng ký tự cần xử lý:

```python
str.maketrans("", "", "!@#$")
# {33: None, 64: None, 35: None, 36: None}    ('!' = 33, '@' = 64, '#' = 35, '$' = 36)
```

Giá trị `None` nghĩa là **xóa ký tự đó**. Sau đó `text.translate(table)` duyệt chuỗi **một lần duy nhất**: với mỗi ký tự, tra bảng (thời gian O(1)), có trong bảng thì xóa hoặc thay, không có thì giữ nguyên.

Vì sao nhanh hơn vòng lặp:
- **Một lần quét** cho mọi ký tự rác. Nếu dùng `replace` thì phải gọi 4 lần (`replace("!", "")`, `replace("@", "")`...), mỗi lần quét lại toàn bộ chuỗi và tạo một chuỗi mới.
- Vòng lặp `for` tự viết bằng Python, nối từng ký tự `result += ch`, sẽ tạo rất nhiều chuỗi trung gian (do chuỗi bất biến) và chạy ở tốc độ trình thông dịch. `translate` được viết bằng **C** bên trong Python.
- Bảng `CLEAN_TABLE` được tạo **một lần** ở đầu chương trình và dùng lại cho mọi lần nạp log.

### Input / Output các hàm

| Hàm | Input | Output |
|---|---|---|
| `clean_raw_logs(raw_text)` | `str` log thô | `list[str]` log đã làm sạch |
| `filter_alert_logs(logs)` | `list[str]` | `list[str]` log ERROR / CRITICAL |
| `is_ip_address(word)` | `str` | `bool`: 4 phần số 0-255 |
| `mask_ip(ip_address)` | `str` | `str` dạng `a.b.*.*` |
| `mask_ip_logs(logs)` | `list[str]` | `list[str]` mới đã che IP |
| `main()` | không | `None` |

### Các dòng List Comprehension

```python
# làm sạch + tách log, bỏ phần rỗng
[" ".join(line.split()) for line in cleaned_text.split(";") if line.strip() != ""]
# lọc cảnh báo không phân biệt hoa thường
[log for log in logs if any(keyword in log.upper() for keyword in ALERT_KEYWORDS)]
# mã hóa IP từng dòng
[" ".join(mask_ip(word) if is_ip_address(word) else word for word in log.split()) for log in logs]
```

## (2) Triển khai code

File: [`security_log_analyzer.py`](security_log_analyzer.py)

```python
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
```

## Kết quả

```
Chọn chức năng (1-4): 2
--- LỌC CẢNH BÁO ---
Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.

Chọn chức năng (1-4): 3
--- MÃ HÓA IP ---
Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.

Chọn chức năng (1-4): 1
--- NẠP DỮ LIỆU LOG ---
Nhập chuỗi log thô (cách nhau bởi dấu ;): ERROR 192.168.1.1 Failed@ login; INFO 10.0.0.5 System start#ed
Đã làm sạch và lưu 2 dòng log vào hệ thống.

Chọn chức năng (1-4): 2
--- LỌC CẢNH BÁO ---
Tìm thấy 1 cảnh báo nguy hiểm:
- ERROR 192.168.1.1 Failed login

Chọn chức năng (1-4): 3
--- MÃ HÓA IP ---
Báo cáo log an toàn:
1. ERROR 192.168.*.* Failed login

Chọn chức năng (1-4): 1
--- NẠP DỮ LIỆU LOG ---
Nhập chuỗi log thô (cách nhau bởi dấu ;): critical Disk$ full on server!!; error Timeout from 172.16.254.3; Error Config file missing; ; warn 8.8.8.8 slow#
Đã làm sạch và lưu 4 dòng log vào hệ thống.

Chọn chức năng (1-4): 2
--- LỌC CẢNH BÁO ---
Tìm thấy 4 cảnh báo nguy hiểm:
- ERROR 192.168.1.1 Failed login
- critical Disk full on server
- error Timeout from 172.16.254.3
- Error Config file missing

Chọn chức năng (1-4): 3
--- MÃ HÓA IP ---
Báo cáo log an toàn:
1. ERROR 192.168.*.* Failed login
2. critical Disk full on server
3. error Timeout from 172.16.*.*
4. Error Config file missing

Chọn chức năng (1-4): 1
--- NẠP DỮ LIỆU LOG ---
Nhập chuỗi log thô (cách nhau bởi dấu ;):  ;  ; 
Không có dòng log hợp lệ nào được nhập.

Chọn chức năng (1-4): 5
Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!

Chọn chức năng (1-4): 4
Đã đóng hệ thống Security Log Analyzer. Tạm biệt!
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Bẫy 1 | Chọn 2, 3 khi chưa nạp log | Chưa có dữ liệu log, vui lòng thực hiện chức năng 1. |
| Nạp log mẫu | `ERROR 192.168.1.1 Failed@ login; INFO 10.0.0.5 System start#ed` | Lưu 2 dòng, `Failed@` → `Failed`, `start#ed` → `started` (khớp đề) |
| Lọc cảnh báo | Chọn 2 | 1 cảnh báo: ERROR 192.168.1.1 Failed login (khớp đề) |
| Mã hóa IP | Chọn 3 | ERROR 192.168.*.* Failed login (khớp đề) |
| Không phân biệt hoa thường | `critical`, `error`, `Error` | Đều được lọc |
| Bẫy 2 - log không có IP | `critical Disk full on server` | Giữ nguyên, không lỗi |
| Đoạn log rỗng giữa `;` | `...; ; warn ...`, ` ;  ; ` | Bỏ qua phần rỗng / báo không có log hợp lệ |
| Menu sai / thoát | `5`, `4` | Báo lỗi / thoát |

## Ghi chú

- Log mới được **thêm vào** `raw_logs` (`extend`), không ghi đè các lần nạp trước. Vì `extend` sửa trực tiếp list nên không cần khai báo `global raw_logs`; chỉ `processed_logs` được gán lại nên `main()` khai báo `global processed_logs`.
- Hàm `is_ip_address` kiểm tra đủ 4 phần số và mỗi phần ≤ 255, nên các chuỗi như `v1.2` hay số phiên bản không bị che nhầm.
