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
