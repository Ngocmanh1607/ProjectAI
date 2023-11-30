import support_function as spf
import time


def DFS_search(board, list_check_point):
    start_time = time.time()

    # Kiểm tra nếu đã thắng trong trạng thái ban đầu
    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]

    # Tạo trạng thái ban đầu với bảng game và danh sách kiểm tra điểm
    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]  # Danh sách trạng thái đã thăm
    list_visit = [start_state]  # Danh sách trạng thái sẽ được duyệt

    while len(list_visit) != 0:
        now_state = list_visit.pop()  # Lấy trạng thái hiện tại từ ngăn xếp

        # Tìm vị trí hiện tại của người chơi trên bảng game
        cur_pos = spf.find_position_player(now_state.board)

        # Lấy danh sách các vị trí mà người chơi có thể di chuyển đến
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos,
                                 cur_pos, list_check_point)

            # Kiểm tra xem trạng thái mới đã được duyệt trước đó chưa
            if spf.is_board_exist(new_board, list_state):
                continue

            # Kiểm tra xem trạng thái mới có khả năng thắng không
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            # Kiểm tra xem tất cả các hộp đã bị kẹt hay chưa
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            # Tạo một trạng thái mới
            new_state = spf.state(new_board, now_state, list_check_point)

            # Kiểm tra xem đã thắng trong trạng thái mới không
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            # Thêm trạng thái mới vào danh sách đã thăm và danh sách sẽ được duyệt tiếp
            list_state.append(new_state)
            list_visit.append(new_state)

            end_time = time.time()

            # Kiểm tra thời gian đã trôi qua, nếu vượt quá giới hạn thì dừng tìm kiếm
            if end_time - start_time > spf.TIME_OUT:
                return []

    # In thông báo nếu không tìm thấy đường đi
    print("Not Found")
    return []
