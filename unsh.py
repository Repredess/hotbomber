import requests
import json

# URL вашего сервера
url = 'http://127.0.0.1:5000'


def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))


# def open_cell(row, col):
#     payload = {'row': row, 'col': col}
#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         board = response.json()['board']
#         print_board(board)
#     else:
#         print('Ошибка при запросе к серверу:', response.status_code)

def start_game(difficulty=1):
    if difficulty == 1:
        payload = {'difficulty': 'easy'}
    elif difficulty == 2:
        payload = {'difficulty': 'medium'}
    elif difficulty == 3:
        payload = {'difficulty': 'hard'}
    response = requests.post(f'{url}/restart', json=payload)
    if response.status_code == 200:
        board = response.json()['board']
        print_board(board)
    else:
        print('Ошибка при запросе к серверу:', response.status_code)


def make_turn(x, y):
    payload = {"row": x, "column": y}
    response = requests.post(f'{url}/click', json=payload)
    if response.status_code == 200:
        print(response)
        board = response.json()['board']
        print_board(board)
    else:
        print('Ошибка при запросе к серверу:', response.status_code)


def toggle_flag():
    response = requests.post(f'{url}/toggle_flag_mode')
    if response.status_code == 200:
        board = response.json()['board']
        print_board(board)
    else:
        print('Ошибка при запросе к серверу:', response.status_code)


def get_board():
    response = requests.post(f'{url}/get_board')
    if response.status_code == 200:
        board = response.json()['board']
        print_board(board)
    else:
        print('Ошибка при запросе к серверу:', response.status_code)


def game():
    while True:
        a = int(input('1. Restart game\n2. Make turn\n3. Toggle flag\n4. See map\n>>>'))
        if a == 1:
            a = int(input('1. Easy\n2. Medium\n3. Hard\n>>>'))
            start_game(difficulty=a)
        if a == 2:
            x, y = int(input('X:\n>>>')), int(input('Y:\n>>>'))
            make_turn(x, y)
        if a == 3:
            toggle_flag()
        if a == 4:
            get_board()


# if __name__ == '__main__':
#     # Пример открытия клетки в 1-й строке и 1-й колонке
#     # open_cell(0, 0)
#     game()


board = input().json()['board']

def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))