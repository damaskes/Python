import tkinter as tk
from random import randint

random_array = [[(1 if randint(0, 5) == 1 else 0) for _ in range(30)] for _ in range(30)]


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Life')
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack()
        self.zone = random_array

    def paint(self):
        self.canvas.delete(tk.ALL)
        for y in range(30):
            for x in range(30):
                nb = 0
                if y > 0 and x > 0 and self.zone[y - 1][x - 1] == 1:
                    nb += 1
                if y < 29 and x < 29 and self.zone[y + 1][x + 1] == 1:
                    nb += 1
                if y < 29 and x > 0 and self.zone[y + 1][x - 1] == 1:
                    nb += 1
                if y > 0 and x < 29 and self.zone[y - 1][x + 1] == 1:
                    nb += 1
                if y > 0 and self.zone[y - 1][x] == 1:
                    nb += 1
                if y < 29 and self.zone[y + 1][x] == 1:
                    nb += 1
                if x > 0 and self.zone[y][x - 1] == 1:
                    nb += 1
                if x < 29 and self.zone[y][x + 1] == 1:
                    nb += 1

                if self.zone[y][x] == 1:
                    if 1 < nb < 4:
                        self.canvas.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill='green')
                    else:
                        self.zone[y][x] = 0
                else:
                    if nb == 3:
                        self.zone[y][x] = 1
                        self.canvas.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill='green')
                    else:
                        self.zone[y][x] = 0
        self.canvas.after(100, self.paint)

    def run(self):
        self.paint()
        self.mainloop()


if __name__ == '__main__':
    Game().run()
