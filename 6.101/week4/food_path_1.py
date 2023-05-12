##### FREE FOOD BONANZA!

from find_path import find_path
import time


def free_food_bonanza(board):
    """
    You belong to a student group that is investing in writing a Python program
    to plot out the shortest path through space to collect all the free food
    that is available at some moment in time.  Write a function that takes in a
    two-dimensional grid with positions of free food and a hungry student.  The
    function should return the minimum number of steps needed for the student to
    enter all of the squares with food.  The student can move up, down, left, or
    right on any given step.  If the student has no way to collect all the food,
    return None.
    
    The grid comes in as a nested list, where each cell holds one of:
    - 'S' for student (exactly one on the board)
    - 'F' for food (arbitrarily many on the board)
    - 'W' for wall (arbitrarily many on the board, student may not walk thru them)
    - ' ' for an empty square
    """
    
    def make_state_from_board(board):
        return tuple(tuple(row) for row in board)

    def find_student(state):
        for r, row in enumerate(state):
            for c, character in enumerate(row):
                if character == 'S':
                    return r,c
        assert False, 'student is gone!'

    def can_move_to(state, r, c):
        return 0 <= r < len(state) and 0 <= c < len(state[0]) and state[r][c] != 'W'
    
    def move_student(state, oldr, oldc, newr, newc):
        assert state[oldr][oldc] == 'S'
        next_board = [[v for v in row] for row in state]
        next_board[oldr][oldc] = ' '
        next_board[newr][newc] = 'S'
        return make_state_from_board(next_board)

    def count_food(state):
        return sum(v == 'F' for row in state for v in row)

    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def neighbors(state):
        """
        Returns iterable of states that can be reached in one move from
        state.
        """
        sr, sc = find_student(state)
        return [
            move_student(state, sr, sc, sr+dr, sc+dc)
                for dr, dc in possible_moves
                if can_move_to(state, sr+dr, sc+dc)
        ]
            
    def goal(state):
        """
        Returns truthy if food is all gone!
        """
        return count_food(state) == 0

    start = make_state_from_board(board)
    path = find_path(neighbors, start, goal)
    return len(path)-1 if path else None


def test_small():
    ## Small boards

    board1 = [['S', ' ', ' ', ' ', 'F']]

    board2 = [['F', ' ', ' ', ' ', ' '],
              ['W', 'W', 'S', 'W', 'F'],
              [' ', ' ', ' ', 'W', ' ']]

    board3 = [['W', ' ', ' ', 'W', 'F'],
              ['W', 'W', ' ', ' ', 'F'],
              ['W', ' ', ' ', ' ', ' '],
              [' ', 'S', 'F', ' ', ' '],
              ['F', 'F', 'F', ' ', ' ']]

    expected_results = [4, 8, 10]

    for b, r in zip([board1, board2, board3], expected_results):
        assert free_food_bonanza(b) == r


def test_large():
    board_sizes = [10, 20, 40, 80]
    for N in board_sizes:
        board = [[' ' for _ in range(N)] for _ in range(N)]
        board[0][0] = 'S'
        board[N-1][N-1] = 'F'
        board[N//2][N//2] = 'W'
        print(f'\nTesting Board Size: {N}')
        start = time.time()
        out = free_food_bonanza(board)
        print(f'Run Took: {time.time() - start} sec')
        assert out == 2*(N-1)
  

if __name__ == '__main__':
    test_small()
    test_large()
