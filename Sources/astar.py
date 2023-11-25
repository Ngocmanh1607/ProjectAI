
import support_function as spf
import time
from queue import PriorityQueue

# Định nghĩa hàm tìm kiếm A*.


def AStar_Search(board, list_check_point):
    start_time = time.time()  # Lưu thời gian bắt đầu tìm kiếm.

    # Kiểm tra xem trạng thái hiện tại đã là trạng thái chiến thắng chưa.
    if spf.check_win(board, list_check_point):
        # Nếu đã thắng, in ra thông báo và trả về bảng hiện tại.
        print("Found win")
        return [board]

    # Khởi tạo trạng thái ban đầu với bảng hiện tại.
    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]  # Lưu danh sách các trạng thái đã thăm.

    # Sử dụng hàng đợi ưu tiên (PriorityQueue) cho việc lựa chọn trạng thái tiếp theo.
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)  # Đưa trạng thái ban đầu vào hàng đợi.

    # Lặp cho đến khi hàng đợi rỗng.
    while not heuristic_queue.empty():
        # Lấy trạng thái có độ ưu tiên cao nhất ra.
        now_state = heuristic_queue.get()
        # Tìm vị trí của người chơi.
        cur_pos = spf.find_position_player(now_state.board)
        # Lấy danh sách các bước di chuyển có thể.
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        # Duyệt qua từng bước di chuyển có thể.
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos,
                                 cur_pos, list_check_point)

            # Kiểm tra các điều kiện để loại bỏ bảng không mong muốn.
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            # Tạo trạng thái mới và kiểm tra chiến thắng.
            new_state = spf.state(new_board, now_state, list_check_point)
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            # Thêm trạng thái mới vào danh sách và hàng đợi.
            list_state.append(new_state)
            heuristic_queue.put(new_state)

            # Kiểm tra thời gian thực thi.
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

        # Kiểm tra thời gian thực thi ngoài vòng lặp.
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    # Kết thúc vòng lặp nếu không tìm thấy giải pháp.
    print("Not Found")
    return []
