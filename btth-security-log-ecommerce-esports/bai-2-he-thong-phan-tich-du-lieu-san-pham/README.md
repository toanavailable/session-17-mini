# Bài 2 - Hệ thống phân tích dữ liệu sản phẩm (E-Commerce Analytics)

## Đề bài

Startup thương mại điện tử lấy danh sách sản phẩm từ database lên dưới dạng chuỗi văn bản thô. Cần biến đổi chúng, sắp xếp theo tiêu chí phức tạp (rating cao xuống thấp; bằng nhau thì giá thấp lên cao) và tính tổng giá trị kho hàng, áp dụng `sort(key=...)` với hàm ẩn danh `lambda`, `functools.reduce()`, cùng định dạng số liệu bằng F-String nâng cao và `str.format_map()`.

```python
product_list = [
    "P01-Tai Nghe Bluetooth-550000-4.5",
    "P02-Chuột Không Dây-250000-4.8",
    "P03-Bàn Phím Cơ-850000-4.5"
]
```

### Menu

```
============ E-COMMERCE ANALYTICS ============
1. Hiển thị tem nhãn sản phẩm (format_map & F-String)
2. Sắp xếp sản phẩm thông minh (sort key)
3. Tính tổng giá trị kho hàng (reduce)
4. Đóng hệ thống
==============================================
Chọn chức năng (1-4):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Tem nhãn | `display_labels(products)` | `split("-")` tách thuộc tính; template chuỗi + `str.format_map()` với dict tạm; giá có dấu phẩy ngăn cách hàng nghìn `{{:,}}`, mã căn trái 10 ký tự |
| 2. Sắp xếp thông minh | `sort_products(products)` + `get_sort_key()` | `list.sort(key=lambda ...)`: Rating giảm dần, bằng nhau thì Giá tăng dần |
| 3. Tổng giá trị kho | `calculate_total_value(products)` | List Comprehension trích giá (int) → `functools.reduce()` cộng dồn → **return** tổng |
| 4. Đóng hệ thống | `main()` | In thông báo kết thúc |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 - Data Integrity | Chuỗi thiếu trường: `P04-Sac Du Phong-300000` | Kiểm tra số phần sau `split` trước khi truy cập index (tránh `IndexError`): "Bỏ qua sản phẩm [P04] do sai cấu trúc dữ liệu" |
| Bẫy 2 - Type Casting | Giá dính chữ: `250000VND` | Kiểm tra `.isdigit()` trước khi `int()` / `float()`, bỏ qua sản phẩm thay vì crash |

## (1) Phân tích và thiết kế

### Hàm `key` trong `sort()` hoạt động thế nào?

`list.sort(key=f)` gọi `f(phần_tử)` **một lần cho mỗi phần tử** để tạo ra "khóa so sánh", rồi sắp xếp các phần tử theo khóa đó (thuật toán Timsort, sắp xếp tại chỗ). Bản thân phần tử (chuỗi gốc) không bị biến đổi, chỉ được sắp theo khóa.

```python
products.sort(key=lambda item: get_sort_key(item))
# get_sort_key("P01-Tai Nghe Bluetooth-550000-4.5") -> (0, -4.5, 550000)
```

### Vì sao trả về tuple `(-rating, price)` giải quyết được 2 tiêu chí ngược chiều?

- Python so sánh tuple **theo thứ tự từ trái sang phải** (so sánh kiểu từ điển): so phần tử đầu, nếu bằng nhau mới so phần tử thứ hai.
- `sort()` mặc định sắp **tăng dần**. Đổi dấu rating thành `-rating` thì rating lớn trở thành số nhỏ hơn (`-4.8 < -4.5`), nên được xếp trước: rating đã **giảm dần**.
- Phần tử thứ hai `price` giữ nguyên dấu nên khi rating bằng nhau, giá được xếp **tăng dần**.

```
P02: (0, -4.8, 250000)   ← -4.8 nhỏ nhất -> đứng đầu
P01: (0, -4.5, 550000)   ┐ cùng -4.5 -> so giá: 550000 < 850000
P03: (0, -4.5, 850000)   ┘
```

- Phần tử `0` ở đầu tuple dành cho sản phẩm hợp lệ; sản phẩm lỗi nhận khóa `(1, 0, 0)` nên luôn bị đẩy xuống cuối mà không làm `sort()` bị lỗi.

### Cơ chế cộng dồn accumulator của `reduce()`

```python
functools.reduce(lambda total, price: total + price, [550000, 250000, 850000], 0)
```

`reduce` giữ một biến tích lũy (accumulator) `total`, khởi tạo bằng giá trị thứ 3 (`0`), rồi lần lượt "gộp" từng phần tử vào:

```
bước 1: total = 0        + 550000 = 550000
bước 2: total = 550000   + 250000 = 800000
bước 3: total = 800000   + 850000 = 1650000   -> kết quả trả về
```

Giá trị khởi tạo `0` giúp `reduce` không lỗi khi danh sách giá rỗng (trả về 0).

### Input / Output các hàm

| Hàm | Input | Output |
|---|---|---|
| `parse_product(product_str)` | `str` | `(tuple | None, str lỗi)` |
| `display_labels(products)` | `list[str]` | `int` số tem đã in |
| `get_sort_key(product_str)` | `str` | `tuple` khóa sắp xếp |
| `sort_products(products)` | `list[str]` | `None` (sắp xếp tại chỗ) |
| `calculate_total_value(products)` | `list[str]` | `int` tổng giá trị |
| `print_sorted_list(products)` | `list[str]` | `None` (in kèm ghi chú) |

## (2) Triển khai code

File: [`ecommerce_analytics.py`](ecommerce_analytics.py)

```python
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
```

## Kết quả

Với dữ liệu mẫu của đề:

```
Chọn chức năng (1-4): 1
--- DANH SÁCH TEM NHÃN ---
Mã: P01        | Tên: Tai Nghe Bluetooth   | Giá: 550,000 VND | Rating: 4.5*
Mã: P02        | Tên: Chuột Không Dây      | Giá: 250,000 VND | Rating: 4.8*
Mã: P03        | Tên: Bàn Phím Cơ          | Giá: 850,000 VND | Rating: 4.5*

Chọn chức năng (1-4): 2
--- SẮP XẾP SẢN PHẨM ---
Đã sắp xếp thành công! Cập nhật danh sách:
1. P02-Chuột Không Dây-250000-4.8
2. P01-Tai Nghe Bluetooth-550000-4.5  (Cùng 4.5* nhưng giá rẻ hơn)
3. P03-Bàn Phím Cơ-850000-4.5

Chọn chức năng (1-4): 3
--- TỔNG GIÁ TRỊ KHO ---
Tổng giá trị các mặt hàng hiện tại là: 1,650,000 VND.

Chọn chức năng (1-4): x
Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!

Chọn chức năng (1-4): 4
Đã đóng hệ thống E-Commerce Analytics. Hẹn gặp lại!
```

Kiểm thử bẫy dữ liệu: thêm 3 sản phẩm (1 thiếu trường, 1 giá dính chữ, 1 hợp lệ) rồi gọi trực tiếp các hàm:

```
>>> Dữ liệu thử nghiệm có lỗi: ['P04-Sac Du Phong-300000', 'P05-Loa Mini-250000VND-4.0', 'P06-Webcam HD-450000-4.8']

>>> Chức năng 1:
--- DANH SÁCH TEM NHÃN ---
Mã: P01        | Tên: Tai Nghe Bluetooth   | Giá: 550,000 VND | Rating: 4.5*
Mã: P02        | Tên: Chuột Không Dây      | Giá: 250,000 VND | Rating: 4.8*
Mã: P03        | Tên: Bàn Phím Cơ          | Giá: 850,000 VND | Rating: 4.5*
[!] Bỏ qua sản phẩm [P04] do sai cấu trúc dữ liệu
[!] Bỏ qua sản phẩm [P05] do giá tiền / đánh giá không phải số
Mã: P06        | Tên: Webcam HD            | Giá: 450,000 VND | Rating: 4.8*

>>> Chức năng 2:
Đã sắp xếp thành công! Cập nhật danh sách:
1. P02-Chuột Không Dây-250000-4.8  (Cùng 4.8* nhưng giá rẻ hơn)
2. P06-Webcam HD-450000-4.8
3. P01-Tai Nghe Bluetooth-550000-4.5  (Cùng 4.5* nhưng giá rẻ hơn)
4. P03-Bàn Phím Cơ-850000-4.5
5. P04-Sac Du Phong-300000  [!] Bỏ qua sản phẩm [P04] do sai cấu trúc dữ liệu
6. P05-Loa Mini-250000VND-4.0  [!] Bỏ qua sản phẩm [P05] do giá tiền / đánh giá không phải số

>>> Chức năng 3: 2,100,000 VND (chỉ cộng sản phẩm hợp lệ)
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Tem nhãn | Chọn 1 | Giá `550,000 VND`, mã căn trái 10 ký tự (khớp đề) |
| Sắp xếp | Chọn 2 | P02 (4.8) → P01 (4.5, rẻ hơn) → P03 (khớp đề) |
| Tổng kho | Chọn 3 | 1,650,000 VND (khớp đề) |
| Bẫy 1 | `P04-Sac Du Phong-300000` | Bỏ qua, không `IndexError` |
| Bẫy 2 | `P05-Loa Mini-250000VND-4.0` | Bỏ qua, không `ValueError` |
| Sắp xếp có dữ liệu lỗi | 6 sản phẩm | 4 sản phẩm hợp lệ xếp đúng, 2 sản phẩm lỗi ở cuối |
| Tổng có dữ liệu lỗi | 6 sản phẩm | 2,100,000 VND (chỉ cộng sản phẩm hợp lệ) |

## Ghi chú

- Dòng `import functools` đặt ở đầu file theo yêu cầu.
- Ghi chú "(Cùng 4.5* nhưng giá rẻ hơn)" trong output mẫu được chương trình tự sinh khi sản phẩm liền sau có cùng rating.
