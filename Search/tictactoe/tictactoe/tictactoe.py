"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    for row in board:
        for cell in row:
            if cell == X:
                countX += 1
            elif cell == O:
                countO += 1
    # Initially, both counts are 0. Therefore X starts.
    if countX > countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    # Iterate through the board and add all empty cells to the set.
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action.")
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = player(board)
    return newBoard   


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check for horizontal wins.
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0] != EMPTY:
            return board[i][0]
        # Check for vertical wins.
        elif (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != EMPTY:
            return board[0][i] 
    # Check for diagonal wins.
    if (board[0][0] == board[1][1] == board[2][2]) and board[0][0] != EMPTY:
        return board[0][0]
    elif (board[0][2] == board[1][1] == board[2][0]) and board[0][2] != EMPTY:
        return board[0][2]
    # No winner.
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if len(actions(board)) == 0:
        return True
    # No empty cells.
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If X has won, return 1.
    if winner(board) == X:
        return 1
    # If O has won, return -1.
    elif winner(board) == O:
        return -1
    # If no one has won, return 0.
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is empty, return None.
    # If the board is terminal, return None.
    if terminal(board):
        return None
    # If the board is not terminal, return the optimal action.
    else:
        if player(board) == X:
            val, act = max_value(board)
            return act
        else:
            val, act = min_value(board)
            return act


def max_value(board):
    """
    Returns the maximum value of a board.
    """
    if terminal(board):
        return utility(board), None
    maxVal = -math.inf
    act = None
    for action in actions(board):
        new, act = min_value(result(board, action))
        if new > maxVal:
            maxVal = new
            act = action
            if maxVal == 1:
                return maxVal, act
    return maxVal, act
        

def min_value(board):
    """
    Returns the minimum value of a board.
    """
    if terminal(board):
        return utility(board), None
    minVal = math.inf
    act = None
    for action in actions(board):
        new, act = max_value(result(board, action))
        if new < minVal:
            minVal = new
            act = action
            if minVal == -1:
                return minVal, act
    return minVal, act