import numpy as np

def can_win(board, player):
    # Check rows
    for row in board:
        if np.count_nonzero(row == player) == 2 and ' ' in row:
            return True

    # Check columns
    for col in range(3):
        if np.count_nonzero(board[:, col] == player) == 2 and ' ' in board[:, col]:
            return True

    # Check diagonals
    diagonal1 = np.diagonal(board)
    diagonal2 = np.fliplr(board).diagonal()
    
    if np.count_nonzero(diagonal1 == player) == 2 and ' ' in diagonal1:
        return True
    if np.count_nonzero(diagonal2 == player) == 2 and ' ' in diagonal2:
        return True

    return False

# Example Tic-Tac-Toe board as a NumPy array
tic_tac_toe_board = np.array([
    ['X', 'O', 'X'],
    [' ', 'X', ' '],
    ['O', ' ', 'X']
])

player = 'X'
if can_win(tic_tac_toe_board, player):
    print(f'Player {player} can win on the next move!')
else:
    print(f'Player {player} cannot win on the next move.')
