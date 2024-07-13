import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows=10, columns=10, mines=10):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.flags = mines
        self.buttons = []
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        game_menu = tk.Menu(menu)
        menu.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Рестарт", command=self.restart)

        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                button = tk.Button(self.master, width=2, height=1, command=lambda r=r, c=c: self.click(r, c))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

        self.flag_button = tk.Button(self.master, text="Флажок", command=self.toggle_flag_mode)
        self.flag_button.grid(row=self.rows, column=0, columnspan=self.columns//2)

        self.restart_button = tk.Button(self.master, text="Рестарт", command=self.restart)
        self.restart_button.grid(row=self.rows, column=self.columns//2, columnspan=self.columns//2)

        self.flag_mode = False
        self.flag_label = tk.Label(self.master, text=f"Флажки: {self.flags}")
        self.flag_label.grid(row=self.rows+1, column=0, columnspan=self.columns)

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
            if self.buttons[r][c]['state'] == 'disabled' or self.buttons[r][c]['text'] == 'F':
                return
            if (r, c) in self.mine_positions:
                self.buttons[r][c].config(text="*", bg="red")
                self.game_over()
                print("Игрок проиграл")
            else:
                self.reveal(r, c)
                if self.check_win():
                    self.win()
                    print("Игрок выиграл")
                else:
                    self.print_board()

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        self.flag_button.config(relief="sunken" if self.flag_mode else "raised")

    def toggle_flag(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled':
            return
        if self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text="")
            self.flags += 1
        else:
            if self.flags > 0:
                self.buttons[r][c].config(text="F")
                self.flags -= 1
        self.flag_label.config(text=f"Флажки: {self.flags}")

    def reveal(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled':
            return
        count = self.count_mines(r, c)
        self.buttons[r][c].config(text=str(count), state="disabled")
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
            self.buttons[r][c].config(text="*", bg="red")
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        self.restart_button.config(state="normal")

    def win(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        self.restart_button.config(state="normal")

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.buttons[r][c]['state'] == 'normal' and (r, c) not in self.mine_positions:
                    return False
        return True

    def restart(self):
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal", bg="SystemButtonFace")
        self.place_mines()
        self.flags = self.mines
        self.flag_label.config(text=f"Флажки: {self.flags}")
        self.flag_mode = False
        self.flag_button.config(relief="raised")
        self.restart_button.config(state="disabled")
        print("Игра перезапущена")

    def print_board(self):
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                if self.buttons[r][c]['state'] == 'disabled':
                    row.append(str(self.buttons[r][c]['text']))
                else:
                    row.append("□")
            print(" ".join(row))
        print()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Сапер")
    game = Minesweeper(root)
    root.mainloop()