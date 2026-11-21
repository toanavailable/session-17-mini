# Bài tập thực hành Python - Xử lý chuỗi & list nâng cao: Security Log, E-Commerce, Esports

Tổng hợp 3 bài tập thực hành (BTTH) về **các hàm xử lý chuỗi và list nâng cao**: `str.maketrans` / `translate`, List Comprehension, `str.format_map`, F-String nâng cao, `sort(key=lambda ...)`, `functools.reduce`, `itertools.combinations`. Mỗi bài là một chương trình CLI có menu, chia thành các hàm có docstring đầy đủ và xử lý các bẫy dữ liệu để không bị crash.

## Thứ tự bài tập

| STT | Bài tập | Kiến thức trọng tâm |
|---|---|---|
| 1 | [Hệ thống phân tích nhật ký bảo mật (Security Log Analyzer)](bai-1-he-thong-phan-tich-nhat-ky-bao-mat/) | `maketrans` + `translate` làm sạch ký tự rác; List Comprehension lọc ERROR / CRITICAL; che giấu IP bằng `split` / `join` |
| 2 | [Hệ thống phân tích dữ liệu sản phẩm (E-Commerce Analytics)](bai-2-he-thong-phan-tich-du-lieu-san-pham/) | `format_map` + F-String `{:,}`, `{:<10}`; `sort(key=lambda)` với tuple `(-rating, price)`; `functools.reduce` |
| 3 | [Hệ thống bốc thăm & ghép đội giải đấu (Esports Matchmaker)](bai-3-he-thong-boc-tham-ghep-doi-esports/) | `itertools.combinations` (vòng tròn một lượt); cắt chuỗi `[0:3]` + lấp `{:X<3}`; số thứ tự `{:02d}` |

Mỗi thư mục bài có mã nguồn Python và `README.md` riêng (đề bài, phân tích thiết kế, mã nguồn, kết quả chạy thử, bảng kiểm thử).

## Cách chạy

Yêu cầu Python 3.x (chỉ dùng thư viện chuẩn). Vào thư mục bài cần chạy, ví dụ:

```bash
cd bai-1-he-thong-phan-tich-nhat-ky-bao-mat
python security_log_analyzer.py
```
