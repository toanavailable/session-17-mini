"""E-Commerce Analytics - Hệ thống phân tích dữ liệu sản phẩm."""
import functools

# =====================================================================
# BIẾN TOÀN CỤC: mỗi sản phẩm là một chuỗi "MãSP-Tên-Giá-ĐánhGiá"
# =====================================================================
product_list = [
    "P01-Tai Nghe Bluetooth-550000-4.5",
    "P02-Chuột Không Dây-250000-4.8",
    "P03-Bàn Phím Cơ-850000-4.5",
]

LABEL_TEMPLATE = "Mã: {code} | Tên: {name} | Giá: {price} VND | Rating: {rating}*"


def parse_product(product_str):
    """Tách chuỗi sản phẩm và kiểm tra tính hợp lệ.

    Tham số:
        product_str (str): chuỗi dạng "MãSP-Tên-Giá-ĐánhGiá"
    Trả về:
        tuple (product, error):
            product: tuple (code: str, name: str, price: int, rating: float) hoặc None nếu lỗi
            error (str): thông báo lỗi, chuỗi rỗng nếu hợp lệ
    """
    parts = product_str.split("-")
    code = parts[0]
    if len(parts) != 4:                                                   # Bẫy 1: thiếu trường
        return None, f"Bỏ qua sản phẩm [{code}] do sai cấu trúc dữ liệu"
    price_text, rating_text = parts[2].strip(), parts[3].strip()
    if not price_text.isdigit() or not rating_text.replace(".", "", 1).isdigit():   # Bẫy 2
        return None, f"Bỏ qua sản phẩm [{code}] do giá tiền / đánh giá không phải số"
    return (code, parts[1], int(price_text), float(rating_text)), ""


def display_labels(products):
    """In tem nhãn từng sản phẩm bằng str.format_map() và F-String.

    Tham số:
        products (list[str]): danh sách chuỗi sản phẩm
    Trả về:
        int: số tem nhãn đã in thành công
    """
    print("--- DANH SÁCH TEM NHÃN ---")
    printed = 0
    for product_str in products:
        product, error = parse_product(product_str)
        if product is None:
            print(f"[!] {error}")
            continue
        code, name, price, rating = product
        label_data = {                                    # dict tạm cho format_map
            "code": f"{code:<10}",                        # căn trái 10 ký tự
            "name": f"{name:<20}",
            "price": f"{price:>7,}",                      # dấu phẩy ngăn cách hàng nghìn, căn phải
            "rating": rating,
        }
        print(LABEL_TEMPLATE.format_map(label_data))
        printed += 1
    return printed


def get_sort_key(product_str):
    """Tạo khóa sắp xếp: Rating giảm dần, nếu bằng nhau thì Giá tăng dần.

    Tham số:
        product_str (str): chuỗi sản phẩm
    Trả về:
        tuple: (0, -rating, price) với sản phẩm hợp lệ;
               (1, 0, 0) với sản phẩm lỗi để đẩy xuống cuối danh sách
    """
    product, _ = parse_product(product_str)
    if product is None:
        return (1, 0, 0)
    return (0, -product[3], product[2])


def sort_products(products):
    """Sắp xếp tại chỗ danh sách sản phẩm bằng list.sort(key=...).

    Tham số:
        products (list[str]): danh sách cần sắp xếp (bị sửa trực tiếp)
    Trả về:
        None
    """
    products.sort(key=lambda item: get_sort_key(item))


def calculate_total_value(products):
    """Tính tổng giá trị kho bằng List Comprehension + functools.reduce().

    Tham số:
        products (list[str]): danh sách chuỗi sản phẩm
    Trả về:
        int: tổng giá tiền của các sản phẩm hợp lệ
    """
    parsed = [parse_product(item)[0] for item in products]
    prices = [product[2] for product in parsed if product is not None]
    return functools.reduce(lambda total, price: total + price, prices, 0)


def print_sorted_list(products):
    """In danh sách sau khi sắp xếp, ghi chú các sản phẩm cùng rating nhưng rẻ hơn."""
    print("Đã sắp xếp thành công! Cập nhật danh sách:")
    for index, product_str in enumerate(products):
        note = ""
        current, error = parse_product(product_str)
        if current is None:
            note = f"  [!] {error}"
        elif index + 1 < len(products):
            following, _ = parse_product(products[index + 1])
            if following is not None and following[3] == current[3]:
                note = f"  (Cùng {current[3]}* nhưng giá rẻ hơn)"
        print(f"{index + 1}. {product_str}{note}")


def main():
    """Vòng lặp menu chính."""
    while True:
        print("\n============ E-COMMERCE ANALYTICS ============")
        print("1. Hiển thị tem nhãn sản phẩm (format_map & F-String)")
        print("2. Sắp xếp sản phẩm thông minh (sort key)")
        print("3. Tính tổng giá trị kho hàng (reduce)")
        print("4. Đóng hệ thống")
        print("=" * 46)
        choice = input("Chọn chức năng (1-4): ").strip()

        if choice in ["1", "2", "3"] and len(product_list) == 0:
            print("Danh sách sản phẩm đang trống.")
        elif choice == "1":
            display_labels(product_list)
        elif choice == "2":
            print("--- SẮP XẾP SẢN PHẨM ---")
            sort_products(product_list)
            print_sorted_list(product_list)
        elif choice == "3":
            print("--- TỔNG GIÁ TRỊ KHO ---")
            total = calculate_total_value(product_list)
            print(f"Tổng giá trị các mặt hàng hiện tại là: {total:,} VND.")
        elif choice == "4":
            print("Đã đóng hệ thống E-Commerce Analytics. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!")


if __name__ == "__main__":
    main()
