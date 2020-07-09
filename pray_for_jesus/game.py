import pygame as pg
import os
from random import randint, choice


class Game:
    def __init__(self):
        self.SIZE = (500, 500)
        self.plays = True
        self.screen = PlayScreen(self)
        self.clock = pg.time.Clock()
        pg.init()
        pg.mixer.init()
        pg.mixer.music.load(os.path.join('data', 'halelujah.mp3'))
        self.window = pg.display.set_mode(self.SIZE)
        pg.display.set_caption('Pray for Jesus')
        pg.mixer.music.play(-1)
        self.mouse_pos = None
        self.is_clicked = None
        self.is_game_stopped = False

    def run(self):
        while self.plays:
            self.is_clicked = False
            self.mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.plays = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.is_clicked = True
            self.screen.render()
            self.clock.tick(30)
            pg.display.flip()

        pg.quit()


class PlayScreen:
    def __init__(self, game):
        self.game = game
        self.surface = pg.Surface(self.game.SIZE)
        self.sprites_group = pg.sprite.Group()
        self.sharks_group = pg.sprite.Group()
        self.jesus = Jesus(self)
        self.border = 400
        self.jesus_border = self.border - self.jesus.size[1] + 8
        self.jesus.set_pos((320, self.jesus_border))

        bg = Bg(self, pg.image.load(os.path.join('data', 'bg.png')), 1)
        bg.resize(self.game.SIZE)
        self.sprites_group.add(bg)

        bg1 = bg.copy()
        bg1.set_pos((-bg1.size[0], bg1.rect.y))
        self.sprites_group.add(bg1)

        self.sprites_group.add(self.sharks_group)

        sea = Bg(self, pg.image.load(os.path.join('data', 'water.jpg')), 3)
        sea.resize((self.game.SIZE[0], sea.size[1]))
        sea.set_pos((0, self.border))
        self.sprites_group.add(sea)

        sea1 = sea.copy()
        sea1.set_pos((-bg1.size[0], self.border))
        self.sprites_group.add(sea1)
        self.sprites_group.add(self.jesus)

        self.pray_image = pg.image.load(os.path.join('data', 'pray.png'))

        self.shark_images = [
            pg.image.load(os.path.join('data', 'tile001.png')),
            pg.image.load(os.path.join('data', 'tile002.png')),
            pg.image.load(os.path.join('data', 'tile012.png')),
            pg.image.load(os.path.join('data', 'tile018.png')),
            pg.image.load(os.path.join('data', 'tile019.png')),
        ]

        self.shark_tick = 0

    def init_pray(self):
        x = randint(400, 470)
        pray = Pray(self, self.pray_image)
        pray.set_pos((x, self.game.SIZE[1]))
        self.sprites_group.add(pray)

    def init_shark(self):
        shark = Shark(self)
        shark.rect.x = 0 - shark.size[0]
        shark.rect.y = self.border - 45
        self.sharks_group.add(shark)

    def update(self):
        if not self.game.is_game_stopped:
            self.shark_tick += 1
            if self.shark_tick == 360:
                self.shark_tick = 0
                self.init_shark()
            self.sharks_group.update()
            self.sprites_group.update()

    def render(self):
        self.update()
        self.surface.fill(pg.Color('red'))
        self.sprites_group.draw(self.surface)
        self.sharks_group.draw(self.surface)
        self.game.window.blit(self.surface, (0, 0))


class SimpleActor(pg.sprite.Sprite):
    def __init__(self, screen, image, *groups):
        super().__init__(*groups)
        self._img = image
        self.screen = screen
        self.image = self._img
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

    def resize(self, size):
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Bg(SimpleActor):
    def __init__(self, screen, image, speed, *groups):
        super().__init__(screen, image, *groups)
        self.speed = speed

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.x >= self.size[0]:
            x = self.rect.x - self.size[0]
            self.rect.x = - self.size[0] + x

    def copy(self):
        bg = Bg(self.screen, self._img, self.speed)
        bg.resize(self.size)
        return bg


class Jesus(pg.sprite.Sprite):
    def __init__(self, play_screen, *groups):
        super().__init__(*groups)
        self.play_screen = play_screen
        self.frames = [
            pg.image.load(os.path.join('data', '5.png')),
            pg.image.load(os.path.join('data', '6.png')),
            pg.image.load(os.path.join('data', '7.png')),
            pg.image.load(os.path.join('data', '8.png')),
        ]
        self.frame_id = 0
        self.frames_count = len(self.frames)
        self.tick = 0
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

        self.speed = 1
        self.up_speed = 10

    def update(self, *args):
        self.tick += 1
        if self.tick > 4:
            self.tick = 0
            self.frame_id += 1
            if self.frame_id == self.frames_count:
                self.frame_id = 0
            self.image = self.frames[self.frame_id]

        self.rect.y += self.speed
        if self.play_screen.game.is_clicked:
            self.play_screen.init_pray()
            self.rect.y -= self.up_speed
            if self.rect.y < self.play_screen.jesus_border:
                self.rect.y = self.play_screen.jesus_border

        if self.rect.y > self.play_screen.game.SIZE[1] or pg.sprite.spritecollideany(self, self.play_screen.sharks_group):
            self.play_screen.game.is_game_stopped = True

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Pray(SimpleActor):
    def __init__(self, screen, image, *groups):
        super().__init__(screen, image, *groups)
        self.side_speed = choice((False, True))
        self.tick = 0

    def update(self, *args):
        self.tick += 1
        if not self.side_speed:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        if self.tick == 10:
            self.side_speed = not self.side_speed
            self.tick = 0

        self.rect.y -= 5
        if self.rect.y < - self.size[1]:
            self.kill()


class Shark(pg.sprite.Sprite):
    def __init__(self, play_screen, *groups):
        super().__init__(*groups)
        self.play_screen = play_screen
        self.frames = self.play_screen.shark_images
        self.frame_id = 0
        self.frame_tick = 0
        self.frames_size = len(self.frames)
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.speed = 3

    def update(self, *args):
        self.rect.x += self.speed
        self.frame_tick += 1
        if self.frame_tick == 5:
            self.frame_tick = 0
            self.frame_id += 1
            if self.frame_id == self.frames_size:
                self.frame_id = 0
            self.image = self.frames[self.frame_id]


if __name__ == '__main__':
    Game().run()
