# def main():
#     print("I'm alive!!!")
#
#
# if __name__ == "__main__":
#     main()

import random


def create_board(rows, cols, bombs):
    board = [['X' for _ in range(cols)] for _ in range(rows)]

    bomb_positions = random.sample(range(rows * cols), bombs)
    for pos in bomb_positions:
        row = pos // cols
        col = pos % cols
        board[row][col] = '*'

    return board


def count_adjacent_bombs(board, row, col):
    rows = len(board)
    cols = len(board[0])
    count = 0

    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if board[i][j] == '*':
                count += 1

    return count


def print_board(board):
    for row in board:
        print('X'.join(row))


def play_game(rows, cols, bombs):
    board = create_board(rows, cols, bombs)
    uncovered = [['X' for _ in range(cols)] for _ in range(rows)]

    while True:
        print_board(uncovered)
        row = int(input('Enter row: '))
        col = int(input('Enter column: '))

        if board[row][col] == '*':
            print('Game over! You hit a bomb.')
            print_board(board)
            break

        count = count_adjacent_bombs(board, row, col)
        uncovered[row][col] = str(count)

        if all(board[i][j] != 'X' or uncovered[i][j] != 'X' for i in range(rows) for j in range(cols)):
            print('Congratulations! You won!')
            print_board(board)
            break


play_game(5, 5, 5)
