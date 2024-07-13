import random

class Minesweeper:
    def __init__(self, rows=10, columns=10, mines=10):
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
            self.toggle_flag(r, c)
        else:
            if self.buttons[r][c] == 'F':
                return self.get_board()
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

    def toggle_flag(self, r, c):
        if self.buttons[r][c] == 'F':
            self.buttons[r][c] = '□'
            self.flags += 1
        else:
            if self.flags > 0:
                self.buttons[r][c] = 'F'
                self.flags -= 1

    def reveal(self, r, c):
        if self.buttons[r][c] != '□':
            return
        count = self.count_mines(r, c)
        self.buttons[r][c] = str(count)
        if count == 0:
            for i in range(r-1, r+2):
                for j in range(c-1, c+2):
                    if 0 <= i < self.rows and 0 <= j < self.columns:
                        self.reveal(i, j)

    def count_mines(self, r, c):
        count = 0
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
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

    def restart(self):
        self.buttons = [['□' for _ in range(self.columns)] for _ in range(self.rows)]
        self.place_mines()
        self.flags = self.mines
        self.flag_mode = False
        status = "started" if self.first_game else "restarted"
        self.first_game = False
        return {"status": status, "board": self.get_board()}

    def get_board(self):
        return [row[:] for row in self.buttons]

# Пример использования API
game = Minesweeper()

# Рестарт игры
print(game.restart())

# Переключение режима флажков
game.toggle_flag_mode()

# Клик по клетке (например, по клетке (0, 0))
print(game.click(0, 0))

# Переключение режима флажков
game.toggle_flag_mode()

# Установка флажка на клетку (например, по клетке (1, 1))
print(game.click(1, 1))

# Рестарт игры
print(game.restart())

# Переключение режима флажков
game.toggle_flag_mode()

# Клик по клетке (например, по клетке (0, 0))
print(game.click(0, 0))

# Переключение режима флажков
game.toggle_flag_mode()

# Установка флажка на клетку (например, по клетке (1, 1))
print(game.click(1, 1))
