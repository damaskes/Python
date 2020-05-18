import pygame as pg
import os
from random import randint

import actors


class App:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        pg.mixer.init()
        self.WINDOW_SIZE = (350, 550)
        self.FPS = 30
        self.window = pg.display.set_mode(self.WINDOW_SIZE)
        self.clock = pg.time.Clock()
        pg.mixer.music.load(os.path.join('assets', 'music.mp3'))

        self.jumped = False
        self.is_running = True
        self.mouse_pos = None

        self.scene = Scene(self)

    def run(self):
        pg.mixer.music.play(-1)
        while self.is_running:
            self.mouse_pos = pg.mouse.get_pos()
            self.jumped = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.jumped = True

            self.scene.render()
            pg.display.flip()
            self.clock.tick(self.FPS)

        pg.mixer.quit()
        pg.quit()


class Scene:
    def __init__(self, app):
        self.app = app
        self.surface = pg.Surface(self.app.WINDOW_SIZE)
        self.sprites = pg.sprite.Group()
        self.pipe_sprites = pg.sprite.Group()
        self.pipe_tick = 0  # pipe re spawn timer
        self.is_hero_alive = True  # end of game switch

        self.up_pipe_image = pg.image.load(os.path.join('assets', 'toptube.png'))
        self.down_pipe_image = pg.image.load(os.path.join('assets', 'bottomtube.png'))
        self.game_over_image = pg.image.load(os.path.join('assets', 'gameover.png'))

        bg_image = pg.image.load(os.path.join('assets', 'bg.png'))
        ground_image = pg.image.load(os.path.join('assets', 'ground.png'))
        hero_images = [
            pg.image.load(os.path.join('assets', 'b1.png')),
            pg.image.load(os.path.join('assets', 'b2.png')),
            pg.image.load(os.path.join('assets', 'b3.png')),
            pg.image.load(os.path.join('assets', 'b2.png')),
        ]

        self.play_button = actors.Button(pg.image.load(os.path.join('assets', 'playbtn.png')), self, self.restart)
        self.play_button.set_pos(130, 270)

        bg1 = actors.MovableBg(bg_image, self, 1)
        bg1.set_size(self.app.WINDOW_SIZE)
        self.sprites.add(bg1)
        bg2 = actors.MovableBg(bg_image, self, 1)
        bg2.set_size(self.app.WINDOW_SIZE)
        bg2.set_pos(self.app.WINDOW_SIZE[0], bg2.rect.y)
        self.sprites.add(bg2)

        ground1 = actors.MovableBg(ground_image, self, 2)
        ground1.set_size((self.app.WINDOW_SIZE[0], ground1.size[1]))
        ground1.set_pos(0, self.app.WINDOW_SIZE[1] - ground1.size[1])
        self.sprites.add(ground1)
        ground2 = actors.MovableBg(ground_image, self, 2)
        ground2.set_size((self.app.WINDOW_SIZE[0], ground2.size[1]))
        ground2.set_pos(self.app.WINDOW_SIZE[0], self.app.WINDOW_SIZE[1] - ground1.size[1])
        self.sprites.add(ground2)

        self.hero = actors.Hero(hero_images, self)
        self.hero.set_pos(100, 300)
        self.sprites.add(self.hero)

    def restart(self):
        self.is_hero_alive = True
        self.hero.speed = 0
        self.hero.set_pos(100, 300)
        self.pipe_sprites.empty()

    def generate_pipes(self):
        cons = randint(0, 200)

        up_pipe = actors.Pipe(self.up_pipe_image, self)
        up_pipe.set_size((up_pipe.size[0], up_pipe.size[1] + 100))
        up_pipe.set_pos(self.app.WINDOW_SIZE[0], - cons)
        self.pipe_sprites.add(up_pipe)

        down_pipe = actors.Pipe(self.down_pipe_image, self)
        down_pipe.set_size((down_pipe.size[0], down_pipe.size[1] + 100))
        down_pipe.set_pos(self.app.WINDOW_SIZE[0], up_pipe.rect.y + up_pipe.size[1] + 95)
        self.pipe_sprites.add(down_pipe)

    def update(self):

        # pipe re spawn
        self.pipe_tick += 1
        if self.pipe_tick == 70:
            self.pipe_tick = 0
            self.generate_pipes()

        self.sprites.update()
        self.pipe_sprites.update()

    def render(self):
        self.surface.fill(pg.Color('red'))
        self.sprites.draw(self.surface)
        self.pipe_sprites.draw(self.surface)
        if self.is_hero_alive:
            self.update()
        else:
            self.surface.blit(self.game_over_image, (80, 190))
            self.play_button.update()
            self.surface.blit(self.play_button.image, (self.play_button.rect.x, self.play_button.rect.y))
        self.app.window.blit(self.surface, (0, 0))


if __name__ == '__main__':
    App().run()
