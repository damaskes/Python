import tkinter as tk
from random import randint

CELL = 10
STEPS = 40
UP = 'Up'
DOWN = 'Down'
LEFT = 'Left'
RIGHT = 'Right'


class SnakeGame:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Snake Game on Python/Tkinter')
        self.root.resizable(0, 0)
        self.root.bind('<KeyPress>', self.key_handle)
        self.canvas = tk.Canvas(self.root, width=CELL * STEPS, height=CELL * STEPS, bg='gray')
        self.canvas.pack()

        self.direction = UP
        self.reversed_speed = 300
        self.dx = 0
        self.dy = 0

        self.snake_body = []
        self.snake_body.append(self.generate_random_cord())
        self.target = self.generate_random_cord(target=True)

        self.score = 0
        self.pices = 1
    
    def tick(self):
        if self.direction == UP:
            self.dx = 0
            self.dy = -1
        if self.direction == DOWN:
            self.dx = 0
            self.dy = 1
        if self.direction == LEFT:
            self.dx = -1
            self.dy = 0
        if self.direction == RIGHT:
            self.dx = 1
            self.dy = 0
        
        # add new pice
        self.snake_body.append([self.snake_body[-1][0] + self.dx, self.snake_body[-1][1] + self.dy])

        # eating
        if self.snake_body[-1] == self.target:
            self.pices += 1
            self.score += 1
            self.target = self.generate_random_cord(target=True)
            if self.reversed_speed > 20:
                self.reversed_speed -= 10

        # game over
        if self.snake_body[-1] in self.snake_body[:-1] or self.snake_body[-1][0] == -1 or self.snake_body[-1][0] == STEPS or self.snake_body[-1][1] == -1 or self.snake_body[-1][1] == STEPS:
            self.snake_body = []
            self.snake_body.append(self.generate_random_cord())
            self.target = self.generate_random_cord(target=True)
            self.pices = 1
            self.score = 0
            self.reversed_speed = 300
        
        # slice snake
        self.snake_body = self.snake_body[-self.pices :]

        # render
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(50, 20, text='Score: {}'.format(self.score), fill='gold', font=('Arial 12'))
        self.canvas.create_rectangle(self.target[0] * CELL, self.target[1] * CELL, self.target[0] * CELL + CELL, self.target[1] * CELL + CELL, fill='red')
        [self.canvas.create_rectangle(s[0] * CELL, s[1] * CELL, s[0] * CELL + CELL, s[1] * CELL + CELL, fill='green') for s in self.snake_body]
        self.canvas.after(self.reversed_speed, self.tick)
    
    def generate_random_cord(self, target=False) -> list:
        res = [randint(0, STEPS - 1), randint(0, STEPS - 1)]
        if target:
            if res in self.snake_body:
                self.generate_random_cord()
        return res
    
    def key_handle(self, event) -> None:
        if event.keysym == UP and self.direction == DOWN or event.keysym == DOWN and self.direction == UP or event.keysym == LEFT and self.direction == RIGHT or event.keysym == RIGHT and self.direction == LEFT:
            return
        self.direction = event.keysym
    
    def run(self) -> None:
        self.tick()
        self.root.mainloop()


if __name__ == '__main__':
    SnakeGame().run()
