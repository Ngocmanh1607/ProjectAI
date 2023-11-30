from copy import deepcopy

TIME_OUT = 1800  # Đặt thời gian tối đa cho quá trình tìm kiếm là 1800 giây.

# Lớp định nghĩa trạng thái trong game.


class state:
    def __init__(self, board, state_parent, list_check_point):
        # Khởi tạo trạng thái với bảng game, trạng thái cha và danh sách điểm kiểm tra.
        self.board = board
        self.state_parent = state_parent
        self.cost = 1  # Chi phí mặc định cho mỗi bước di chuyển là 1.
        self.heuristic = 0  # Giá trị heuristic ban đầu là 0.
        # Sao chép danh sách điểm kiểm tra.
        self.check_points = deepcopy(list_check_point)

    # Phương thức lấy toàn bộ chuỗi các trạng thái dẫn đến trạng thái hiện tại.
    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]

    # Tính toán giá trị heuristic cho trạng thái.
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + \
                abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i]
                    [0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic

    # Định nghĩa phép so sánh lớn hơn giữa các trạng thái dựa trên heuristic.
    def __gt__(self, other):
        return self.compute_heuristic() > other.compute_heuristic()

    # Định nghĩa phép so sánh nhỏ hơn giữa các trạng thái dựa trên heuristic.
    def __lt__(self, other):
        return self.compute_heuristic() < other.compute_heuristic()

# Kiểm tra xem bảng game đã đạt đến trạng thái chiến thắng chưa.


def check_win(board, list_check_point):
    for p in list_check_point:
        if board[p[0]][p[1]] != 'b':
            return False
    return True

# Hàm tạo bản sao của bảng game.


def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

# Tìm vị trí của người chơi trên bảng game.


def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'p':
                return (x, y)
    return (-1, -1)  # Trả về (-1, -1) nếu không tìm thấy người chơi.

# So sánh hai bảng game với nhau.


def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

# Kiểm tra xem một bảng game đã tồn tại trong danh sách các trạng thái hay chưa.


def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False

# Kiểm tra xem một hộp có nằm trên điểm kiểm tra không.


def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False

# Kiểm tra xem một hộp có bị kẹt ở góc của bức tường hay không.


def check_in_corner(board, x, y, list_check_point):
    '''return true if board[x][y] in corner'''
    if board[x-1][y-1] == '1':
        if board[x-1][y] == '1' and board[x][y-1] == '1':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x+1][y-1] == '1':
        if board[x+1][y] == '1' and board[x][y-1] == '1':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x-1][y+1] == '1':
        if board[x-1][y] == '1' and board[x][y+1] == '1':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x+1][y+1] == '1':
        if board[x+1][y] == '1' and board[x][y+1] == '1':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    return False

# Tìm vị trí của tất cả các hộp trên bảng.


def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'b':
                result.append((i, j))
    return result

# Kiểm tra xem một hộp có thể di chuyển được không.


def is_box_can_be_moved(board, box_position):
    # Xác định các hướng di chuyển có thể từ vị trí hộp hiện tại.
    # ...
    # Nếu có ít nhất một hướng di chuyển hợp lệ, trả về True. Ngược lại, trả về False.
    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == 't' or board[left_move[0]][left_move[1]] == 'p') and board[right_move[0]][right_move[1]] != '1' and board[right_move[0]][right_move[1]] != 'b':
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == 't' or board[right_move[0]][right_move[1]] == 'p') and board[left_move[0]][left_move[1]] != '1' and board[left_move[0]][left_move[1]] != 'b':
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == 't' or board[up_move[0]][up_move[1]] == 'p') and board[down_move[0]][down_move[1]] != '1' and board[down_move[0]][down_move[1]] != 'b':
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == 't' or board[down_move[0]][down_move[1]] == 'p') and board[up_move[0]][up_move[1]] != '1' and board[up_move[0]][up_move[1]] != 'b':
        return True
    return False


# Kiểm tra xem tất cả các hộp có bị kẹt không.
def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result

# Kiểm tra xem bảng game có còn khả năng chiến thắng không.


def is_board_can_not_win(board, list_check_point):
    '''return true if box in corner of wall -> can't win'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'b':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False

# Lấy danh sách các vị trí mà người chơi có thể di chuyển đến từ vị trí hiện tại.


def get_next_pos(board, cur_pos):
    '''return list of positions that player can move to from current position'''
    x, y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == 't':
            list_can_move.append((x - 1, y))
        elif value == 'b' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '1' and next_pos_box != 'b':
                list_can_move.append((x - 1, y))
    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == 't':
            list_can_move.append((x + 1, y))
        elif value == 'b' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '1' and next_pos_box != 'b':
                list_can_move.append((x + 1, y))
    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == 't':
            list_can_move.append((x, y - 1))
        elif value == 'b' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '1' and next_pos_box != 'b':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == 't':
            list_can_move.append((x, y + 1))
        elif value == 'b' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '1' and next_pos_box != 'b':
                list_can_move.append((x, y + 1))
    return list_can_move


def move(board, next_pos, cur_pos, list_check_point):
    # The line `new_board = assign_matrix(board)` creates a deep copy of the `board` list. It creates
    # a new list with the same values as the `board` list, ensuring that any changes made to
    # `new_board` will not affect the original `board` list.
    new_board = assign_matrix(board)
    if new_board[next_pos[0]][next_pos[1]] == 'b':
        x = 2*next_pos[0] - cur_pos[0]
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = 'b'
    new_board[next_pos[0]][next_pos[1]] = 'p'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = 't'
    return new_board


def find_list_check_point(board):
    list_check_point = []
    num_of_box = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'b':
                num_of_box += 1
            elif board[x][y] == 't':
                list_check_point.append((x, y))
    if num_of_box < len(list_check_point):
        return [(-1, -1)]
    return list_check_point
