from copy import deepcopy

TIME_OUT = 1800


class state:
    def __init__(self, board, state_parent, list_check_point):
        self.board = board
        self.state_parent = state_parent
        self.cost = 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)

    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]

    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + \
                abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i]
                    [0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic

    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else:
            return False


def check_win(board, list_check_point):
    for p in list_check_point:
        if board[p[0]][p[1]] != 'b':
            return False
    return True


def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]


def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'p':
                return (x, y)
    return (-1, -1)  # error board


def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True


def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False


def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False


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


def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'b':
                result.append((i, j))
    return result


def is_box_can_be_moved(board, box_position):
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


def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result


def is_board_can_not_win(board, list_check_point):
    '''return true if box in corner of wall -> can't win'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'b':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False


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
