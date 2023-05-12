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
    def make_state_from_board(board): ...
        
    def neighbors(state): ...
        
    def goal(state): ...
        
    start = make_state_from_board(board)
    path = find_path(neighbors, start, goal)

    return ______________


def find_path(neighbors_function, start, goal_test):
    """ ***find_path from end of graph search reading***
    Given:
        - neighbors_function(state) that returns a list of legal neighbor states
        - start as the starting state for the search
        - goal_test(state) that returns a truthy value if state is a goal state
    Returns a shortest path from start to a state satisfying goal_test(), 
    or None if no path exists.
    State representation is up to the caller, but must be hashable.
    """
    ...
