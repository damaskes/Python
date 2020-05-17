import tkinter as tk
from random import randint


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Life')
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack()
        self.zone = [[(1 if randint(0, 5) == 1 else 0) for _ in range(30)] for _ in range(30)]

    def paint(self):
        self.canvas.delete(tk.ALL)
        for i in range(30):
            for j in range(30):
                nb = 0
                if i > 0 and self.zone[i - 1][j] == 1:
                    nb += 1
                if i < 29 and self.zone[i + 1][j] == 1:
                    nb += 1
                if j > 0 and self.zone[i][j - 1] == 1:
                    nb += 1
                if j < 29 and self.zone[i][j + 1] == 1:
                    nb += 1

                if i > 0 and j > 0 and self.zone[i - 1][j - 1] == 1:
                    nb += 1
                if i < 29 and j < 29 and self.zone[i + 1][j + 1] == 1:
                    nb += 1
                if i < 29 and j > 0 and self.zone[i + 1][j - 1] == 1:
                    nb += 1
                if i > 0 and j < 29 and self.zone[i - 1][j + 1] == 1:
                    nb += 1

                if self.zone[i][j] == 1:
                    if 1 < nb < 4:
                        self.zone[i][j] = 1
                        self.canvas.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill='green')
                    else:
                        self.zone[i][j] = 0
                else:
                    if nb == 3:
                        self.zone[i][j] = 1
                        self.canvas.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill='green')
                    else:
                        self.zone[i][j] = 0
        self.canvas.after(100, self.paint)

    def run(self):
        self.paint()
        self.mainloop()


if __name__ == '__main__':
    Game().run()
