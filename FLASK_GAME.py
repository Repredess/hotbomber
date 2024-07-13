from flask import Flask, request, jsonify
import random

app = Flask(__name__)


class Minesweeper:
    def __init__(self, rows=9, columns=9, mines=10):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.flags = mines
        self.buttons = [['□' for _ in range(columns)] for _ in range(rows)]
        self.mine_positions = set()
        self.flag_mode = False
        self.first_game = True
        self.place_mines()

    def place_mines(self):
        self.mine_positions.clear()
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            self.mine_positions.add((r, c))

    def click(self, r, c):
        if self.flag_mode:
            return self.toggle_flag(r, c)
        else:
            if self.buttons[r][c] == 'F':
                return {"status": "flag_on_cell", "board": self.get_board()}
            if (r, c) in self.mine_positions:
                self.buttons[r][c] = '*'
                return self.game_over()
            else:
                self.reveal(r, c)
                if self.check_win():
                    return self.win()
                else:
                    return self.get_board()

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        return {"status": "flag_mode_toggled", "flag_mode": self.flag_mode}

    def toggle_flag(self, r, c):
        if self.buttons[r][c] == 'F':
            self.buttons[r][c] = '□'
            self.flags += 1
            return {"status": "flag_untoggled", "board": self.get_board(), "flags_left": self.flags}
        elif self.buttons[r][c] == '□':
            if self.flags > 0:
                self.buttons[r][c] = 'F'
                self.flags -= 1
                return {"status": "flag_toggled", "board": self.get_board(), "flags_left": self.flags}
            else:
                return {"status": "flag_limit_reached", "board": self.get_board(), "flags_left": self.flags}
        else:
            return {"status": "cannot_flag_open_cell", "board": self.get_board(), "flags_left": self.flags}

    def reveal(self, r, c):
        if self.buttons[r][c] != '□':
            return
        count = self.count_mines(r, c)
        self.buttons[r][c] = str(count)
        if count == 0:
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if 0 <= i < self.rows and 0 <= j < self.columns:
                        self.reveal(i, j)

    def count_mines(self, r, c):
        count = 0
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if (i, j) in self.mine_positions:
                    count += 1
        return count

    def game_over(self):
        for r, c in self.mine_positions:
            self.buttons[r][c] = '*'
        return {"status": "game_over", "board": self.get_board()}

    def win(self):
        return {"status": "win", "board": self.get_board()}

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.buttons[r][c] == '□' and (r, c) not in self.mine_positions:
                    return False
        return True

    def restart(self, difficulty='easy'):
        if difficulty == 'easy':
            self.rows, self.columns, self.mines = 9, 9, 10
        elif difficulty == 'medium':
            self.rows, self.columns, self.mines = 16, 16, 40
        elif difficulty == 'hard':
            self.rows, self.columns, self.mines = 16, 30, 99
        self.buttons = [['□' for _ in range(self.columns)] for _ in range(self.rows)]
        self.place_mines()
        self.flags = self.mines
        self.flag_mode = False
        status = "started" if self.first_game else "restarted"
        self.first_game = False
        return {"status": status, "board": self.get_board()}

    def get_board(self):
        return [row[:] for row in self.buttons]


game = Minesweeper()


@app.route('/restart', methods=['POST'])
def restart():
    data = request.json
    difficulty = data.get('difficulty', 'easy')
    return jsonify(game.restart(difficulty))


@app.route('/click', methods=['POST'])
def click():
    data = request.json
    r = data['row']
    c = data['column']
    print(jsonify(game.click(r, c)))
    return jsonify(game.click(r, c))


@app.route('/toggle_flag_mode', methods=['POST'])
def toggle_flag_mode():
    return jsonify(game.toggle_flag_mode())


@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({"board": game.get_board()})


if __name__ == '__main__':
    app.run(debug=True)
    # Для развертывания на сервере:
    # app.run(host='0.0.0.0', port=5000, debug=True)

# sudo python3 FLASK_GAME.py
# Примеры запросов
#
# Рестарт игры с выбором уровня сложности:

# curl -X POST http://127.0.0.1:5000/restart -H "Content-Type: application/json" -d '{"difficulty": "medium"}'
#
# Клик по клетке:
#
# curl -X POST http://127.0.0.1:5000/click -H "Content-Type: application/json" -d '{"row": 0, "column": 0}'

# Переключение режима флажков:
#
# curl -X POST http://127.0.0.1:5000/toggle_flag_mode

# Получение текущего поля:
#
# curl -X GET http://127.0.0.1:5000/get_board

# Установка флажка на клетку:
#
# curl -X POST http://127.0.0.1:5000/click -H "Content-Type: application/json" -d '{"row": 1, "column": 1}'

# Если лимит флажков исчерпан, сервер вернет статус "flag_limit_reached",актуальное поле и количество доступных флажков.
# Если попытка поставить флажок на открытую клетку, сервер вернет статус "cannot_flag_open_cell".
# Если флажок убран, сервер вернет статус "flag_untoggled".
# Если пользователь пытается выбрать клетку с флажком в режиме flag_mode: false, сервер вернет статус "flag_on_cell".
