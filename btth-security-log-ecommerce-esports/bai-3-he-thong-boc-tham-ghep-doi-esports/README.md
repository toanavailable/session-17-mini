# Bài 3 - Hệ thống bốc thăm và ghép đội giải đấu (Esports Matchmaker)

## Đề bài

Ban tổ chức giải đấu thể thao điện tử cần phần mềm bốc thăm chia bảng và tạo lịch thi đấu tự động. Từ danh sách đội tuyển, hệ thống tạo **tất cả các cặp đấu** có thể xảy ra (vòng tròn một lượt), rồi tạo **mã định danh (Match ID)** duy nhất cho từng trận. Thay vì vòng lặp lồng nhau, dùng module `itertools` (`combinations`, `permutations`) kết hợp các hàm xử lý String. Biến toàn cục: `teams_list = []`.

### Menu

```
============ ESPORTS MATCHMAKER ============
1. Nhập danh sách đội tuyển
2. Tạo lịch thi đấu (Combinations)
3. Tạo mã trận đấu tự động (F-String & Cắt chuỗi)
4. Đóng hệ thống
============================================
Chọn chức năng (1-4):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Nhập đội tuyển | `input_teams(raw_text)` | `split(",")` + List Comprehension `.strip().upper()` → `teams_list` |
| 2. Tạo lịch thi đấu | `create_schedule(teams)` | `itertools.combinations(teams_list, 2)`; định dạng `"ĐỘI A vs ĐỘI B"`; **return** danh sách trận |
| 3. Tạo mã trận | `generate_match_ids(schedule)` + `make_team_code()` | `split(" vs ")`; cắt `[0:3]`, thiếu thì lấp `X` (`{{:X<3}}`); số thứ tự `{{:02d}}` |
| 4. Đóng hệ thống | `main()` | In thông báo kết thúc |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 | Ít hơn 2 đội khi tạo lịch | "Lỗi: Cần tối thiểu 2 đội để tạo lịch thi đấu." |
| Bẫy 2 | Sinh mã ID khi chưa có lịch | "Vui lòng tạo lịch thi đấu trước khi sinh mã ID." |
| Bẫy 3 | Tên đội trùng (`T1, GEN.G, T1`) | Dùng `set` kiểm tra, loại bỏ tên trùng trước khi lưu |

## (1) Phân tích và thiết kế

### `combinations` (tổ hợp) và `permutations` (chỉnh hợp)

|  | `itertools.combinations(teams, 2)` | `itertools.permutations(teams, 2)` |
|---|---|---|
| Thứ tự trong cặp | **Không quan trọng**: (A, B) = (B, A) | **Có quan trọng**: (A, B) ≠ (B, A) |
| Số cặp với n đội | C(n,2) = n(n−1)/2 | A(n,2) = n(n−1) |
| Với 4 đội | **6 trận** | 12 trận |
| Ví dụ 3 đội | (T1, GEN.G), (T1, WBG), (GEN.G, WBG) | (T1, GEN.G), (GEN.G, T1), (T1, WBG), (WBG, T1)... |

Thể thức **"vòng tròn một lượt"** nghĩa là mỗi cặp đội gặp nhau **đúng một lần**: T1 gặp GEN.G thì không có thêm trận GEN.G gặp T1. Đó chính là định nghĩa tổ hợp chập 2, nên bắt buộc dùng `combinations`. Nếu dùng `permutations`, mỗi cặp xuất hiện 2 lần (giống thể thức sân nhà / sân khách, tức hai lượt), số trận bị gấp đôi và sai thể thức.

`combinations` cũng thay thế hoàn toàn vòng lặp lồng nhau kiểu `for i ... for j in range(i + 1, ...)`: code ngắn, không lo sai chỉ số, và thứ tự các cặp giữ đúng thứ tự nhập đội.

### Luồng thuật toán sinh Match ID

```
VỚI MỖI (số_thứ_tự, trận) trong enumerate(match_schedule, start=1):
    đội_a, đội_b ← trận.split(" vs ")           # "T1 vs GEN.G" -> ["T1", "GEN.G"]
    mã_a ← f"{đội_a[0:3]:X<3}"                   # "T1"[0:3] = "T1" -> căn trái độ rộng 3, lấp "X" -> "T1X"
    mã_b ← f"{đội_b[0:3]:X<3}"                   # "GEN.G"[0:3] = "GEN"
    id   ← f"M{số_thứ_tự:02d}-{mã_a}-{mã_b}"     # 1 -> "01": "M01-T1X-GEN"
```

**Số 0 được thêm vào trước số thứ tự thế nào?** Trong format spec `02d`:
- `d`: định dạng số nguyên thập phân;
- `2`: **độ rộng tối thiểu** là 2 ký tự;
- `0` đứng trước độ rộng: ký tự **lấp đầy là số 0** (thay cho khoảng trắng mặc định), căn phải.

Vì vậy `1` thành `"01"`, `7` thành `"07"`, còn `12` đã đủ 2 chữ số nên giữ nguyên `"12"`. Tương tự `{:X<3}` nghĩa là căn trái (`<`), độ rộng 3, lấp bằng `X`.

### Input / Output các hàm

| Hàm | Input | Output |
|---|---|---|
| `input_teams(raw_text)` | `str` | `(list[str] đội, list[str] tên trùng)` |
| `create_schedule(teams)` | `list[str]` | `list[str]` trận "A vs B" |
| `make_team_code(team_name)` | `str` | `str` 3 ký tự |
| `generate_match_ids(schedule)` | `list[str]` | `list[str]` mã trận |
| `main()` | không | `None` |

## (2) Triển khai code

File: [`esports_matchmaker.py`](esports_matchmaker.py)

```python
"""Esports Matchmaker - Hệ thống bốc thăm và ghép đội giải đấu."""
import itertools

# =====================================================================
# BIẾN TOÀN CỤC
# =====================================================================
teams_list = []          # Danh sách đội tuyển đã chuẩn hóa
match_schedule = []      # Danh sách trận đấu dạng "ĐỘI A vs ĐỘI B"


def input_teams(raw_text):
    """Tách và chuẩn hóa danh sách đội tuyển từ chuỗi nhập.

    Tham số:
        raw_text (str): các tên đội cách nhau bởi dấu phẩy, ví dụ "t1, gen.g ,  wbg"
    Trả về:
        tuple (teams, duplicates):
            teams (list[str]): tên đội đã strip().upper(), bỏ trùng, giữ thứ tự nhập
            duplicates (list[str]): các tên đội bị trùng đã loại bỏ
    """
    names = [name.strip().upper() for name in raw_text.split(",") if name.strip() != ""]
    teams = []
    duplicates = []
    seen = set()                         # set kiểm tra trùng nhanh
    for name in names:
        if name in seen:
            duplicates.append(name)      # Bẫy 3: tên đội trùng lặp
        else:
            seen.add(name)
            teams.append(name)
    return teams, duplicates


def create_schedule(teams):
    """Tạo lịch thi đấu vòng tròn một lượt bằng itertools.combinations.

    Tham số:
        teams (list[str]): danh sách đội tuyển
    Trả về:
        list[str]: các trận dạng "ĐỘI A vs ĐỘI B" (mỗi cặp gặp nhau đúng 1 lần)
    """
    return [f"{team_a} vs {team_b}" for team_a, team_b in itertools.combinations(teams, 2)]


def make_team_code(team_name):
    """Lấy 3 ký tự đầu của tên đội; nếu ngắn hơn 3 ký tự thì lấp đầy bằng "X".

    Tham số:
        team_name (str): tên đội, ví dụ "T1"
    Trả về:
        str: mã 3 ký tự, ví dụ "T1X"
    """
    return f"{team_name[0:3]:X<3}"


def generate_match_ids(schedule):
    """Sinh mã định danh cho từng trận: M + số thứ tự 2 chữ số + mã 2 đội.

    Tham số:
        schedule (list[str]): danh sách trận "ĐỘI A vs ĐỘI B"
    Trả về:
        list[str]: danh sách mã trận, ví dụ "M01-T1X-GEN"
    """
    match_ids = []
    for number, match in enumerate(schedule, start=1):
        team_a, team_b = match.split(" vs ")
        match_ids.append(f"M{number:02d}-{make_team_code(team_a)}-{make_team_code(team_b)}")
    return match_ids


def main():
    """Vòng lặp menu chính."""
    global teams_list, match_schedule
    while True:
        print("\n============ ESPORTS MATCHMAKER ============")
        print("1. Nhập danh sách đội tuyển")
        print("2. Tạo lịch thi đấu (Combinations)")
        print("3. Tạo mã trận đấu tự động (F-String & Cắt chuỗi)")
        print("4. Đóng hệ thống")
        print("=" * 44)
        choice = input("Chọn chức năng (1-4): ").strip()

        if choice == "1":
            print("--- NHẬP DANH SÁCH ---")
            teams, duplicates = input_teams(input("Nhập các đội (cách nhau bởi dấu phẩy): "))
            if duplicates:
                print(f"Đã loại bỏ {len(duplicates)} tên đội bị trùng: {', '.join(duplicates)}")
            teams_list = teams
            match_schedule = []          # danh sách đội mới -> lịch cũ không còn đúng
            print(f"Đã ghi nhận {len(teams_list)} đội: {teams_list}")

        elif choice == "2":
            print("--- LỊCH THI ĐẤU VÒNG BẢNG ---")
            if len(teams_list) < 2:                                           # Bẫy 1
                print("Lỗi: Cần tối thiểu 2 đội để tạo lịch thi đấu.")
                continue
            match_schedule = create_schedule(teams_list)
            for number, match in enumerate(match_schedule, start=1):
                print(f"{number}. {match}")
            print(f"Tổng số trận đấu: {len(match_schedule)} trận.")

        elif choice == "3":
            print("--- MÃ TRẬN ĐẤU (MATCH ID) ---")
            if len(match_schedule) == 0:                                      # Bẫy 2
                print("Vui lòng tạo lịch thi đấu trước khi sinh mã ID.")
                continue
            match_ids = generate_match_ids(match_schedule)
            labels = [f"Trận {number} ({match})" for number, match in enumerate(match_schedule, start=1)]
            width = max(len(label) for label in labels)
            for label, match_id in zip(labels, match_ids):
                print(f"{label:<{width}} -> ID: {match_id}")

        elif choice == "4":
            print("Đã đóng hệ thống Esports Matchmaker. Hẹn gặp lại!")
            break

        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!")


if __name__ == "__main__":
    main()
```

## Kết quả

```
Chọn chức năng (1-4): 2
--- LỊCH THI ĐẤU VÒNG BẢNG ---
Lỗi: Cần tối thiểu 2 đội để tạo lịch thi đấu.

Chọn chức năng (1-4): 3
--- MÃ TRẬN ĐẤU (MATCH ID) ---
Vui lòng tạo lịch thi đấu trước khi sinh mã ID.

Chọn chức năng (1-4): 1
--- NHẬP DANH SÁCH ---
Nhập các đội (cách nhau bởi dấu phẩy): t1
Đã ghi nhận 1 đội: ['T1']

Chọn chức năng (1-4): 2
--- LỊCH THI ĐẤU VÒNG BẢNG ---
Lỗi: Cần tối thiểu 2 đội để tạo lịch thi đấu.

Chọn chức năng (1-4): 1
--- NHẬP DANH SÁCH ---
Nhập các đội (cách nhau bởi dấu phẩy): t1, gen.g ,  wbg, blg
Đã ghi nhận 4 đội: ['T1', 'GEN.G', 'WBG', 'BLG']

Chọn chức năng (1-4): 3
--- MÃ TRẬN ĐẤU (MATCH ID) ---
Vui lòng tạo lịch thi đấu trước khi sinh mã ID.

Chọn chức năng (1-4): 2
--- LỊCH THI ĐẤU VÒNG BẢNG ---
1. T1 vs GEN.G
2. T1 vs WBG
3. T1 vs BLG
4. GEN.G vs WBG
5. GEN.G vs BLG
6. WBG vs BLG
Tổng số trận đấu: 6 trận.

Chọn chức năng (1-4): 3
--- MÃ TRẬN ĐẤU (MATCH ID) ---
Trận 1 (T1 vs GEN.G)  -> ID: M01-T1X-GEN
Trận 2 (T1 vs WBG)    -> ID: M02-T1X-WBG
Trận 3 (T1 vs BLG)    -> ID: M03-T1X-BLG
Trận 4 (GEN.G vs WBG) -> ID: M04-GEN-WBG
Trận 5 (GEN.G vs BLG) -> ID: M05-GEN-BLG
Trận 6 (WBG vs BLG)   -> ID: M06-WBG-BLG

Chọn chức năng (1-4): 1
--- NHẬP DANH SÁCH ---
Nhập các đội (cách nhau bởi dấu phẩy): T1, gen.g, t1, ,DRX, drx
Đã loại bỏ 2 tên đội bị trùng: T1, DRX
Đã ghi nhận 3 đội: ['T1', 'GEN.G', 'DRX']

Chọn chức năng (1-4): 2
--- LỊCH THI ĐẤU VÒNG BẢNG ---
1. T1 vs GEN.G
2. T1 vs DRX
3. GEN.G vs DRX
Tổng số trận đấu: 3 trận.

Chọn chức năng (1-4): 3
--- MÃ TRẬN ĐẤU (MATCH ID) ---
Trận 1 (T1 vs GEN.G)  -> ID: M01-T1X-GEN
Trận 2 (T1 vs DRX)    -> ID: M02-T1X-DRX
Trận 3 (GEN.G vs DRX) -> ID: M03-GEN-DRX

Chọn chức năng (1-4): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4!

Chọn chức năng (1-4): 4
Đã đóng hệ thống Esports Matchmaker. Hẹn gặp lại!
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Bẫy 1 / Bẫy 2 khi chưa có dữ liệu | Chọn 2, 3 | Báo lỗi tương ứng |
| Bẫy 1 - chỉ 1 đội | `t1` | Cần tối thiểu 2 đội |
| Nhập đội | `t1, gen.g ,  wbg, blg` | ['T1', 'GEN.G', 'WBG', 'BLG'] (khớp đề) |
| Bẫy 2 - có đội nhưng chưa tạo lịch | Chọn 3 | Vui lòng tạo lịch thi đấu trước... |
| Tạo lịch | Chọn 2 | 6 trận theo đúng thứ tự (khớp đề) |
| Sinh mã trận | Chọn 3 | M01-T1X-GEN, M02-T1X-WBG ... M06-WBG-BLG (khớp đề) |
| Bẫy 3 - tên trùng, phần rỗng | `T1, gen.g, t1, ,DRX, drx` | Loại 2 tên trùng → 3 đội, 3 trận |
| Menu sai / thoát | `9`, `4` | Báo lỗi / thoát |

## Ghi chú

- `import itertools` đặt ở đầu file; lịch thi đấu tạo bằng `itertools.combinations`, không dùng vòng lặp lồng nhau.
- Khi nhập lại danh sách đội, lịch thi đấu cũ bị xóa (`match_schedule = []`) để tránh sinh mã ID cho lịch không còn đúng.
- Loại trùng dùng `set` để kiểm tra nhanh nhưng vẫn giữ thứ tự nhập đội (không ép cả list thành set, vì set không bảo toàn thứ tự).
