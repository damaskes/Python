import pygame as pg
import os


class SimpleActor(pg.sprite.Sprite):
    def __init__(self, image, scene, *groups):
        super().__init__(*groups)
        self.scene = scene
        self.image = image
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

    def set_size(self, size):
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class MovableBg(SimpleActor):
    def __init__(self, image, scene, speed, *groups):
        super().__init__(image, scene, *groups)
        self.speed = speed

    def update(self, *args):

        # movement
        self.rect.x -= self.speed
        if self.rect.x < - self.scene.app.WINDOW_SIZE[0]:
            pix = self.rect.x + self.scene.app.WINDOW_SIZE[0]
            self.set_pos(self.scene.app.WINDOW_SIZE[0] + pix, self.rect.y)


class Pipe(SimpleActor):
    def __init__(self, image, scene, *groups):
        super().__init__(image, scene, *groups)
        self.speed = 3

    def update(self, *args):

        # movement
        if self.rect.x < - self.size[0]:
            self.kill()
        else:
            self.rect.x -= self.speed


class Button(SimpleActor):
    def __init__(self, image, scene, func, *groups):
        super().__init__(image, scene, *groups)
        self.func = func

    def update(self, *args):
        if self.rect.collidepoint(self.scene.app.mouse_pos):
            if self.scene.app.jumped:
                self.func()


class Hero(pg.sprite.Sprite):
    def __init__(self, images, scene, *groups):
        super().__init__(*groups)
        self.images = images
        self.scene = scene
        self.frame_id = 0
        self.tick = 0
        self.image = self.images[self.frame_id]
        self.rect = self.image.get_rect()
        self._speed = 0
        self.gravity = 0.5
        self.jump_sound = pg.mixer.Sound(os.path.join('assets', 'sfx_wing.ogg'))

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):

        # end of game detection
        if pg.sprite.spritecollideany(self, self.scene.pipe_sprites) or self.rect.y < 0 \
                or self.rect.y > self.scene.app.WINDOW_SIZE[1]:
            self.scene.is_hero_alive = False

        # animation
        self.tick += 1
        if self.tick == 2:
            self.tick = 0
            if self.frame_id == 3:
                self.frame_id = 0
            else:
                self.frame_id += 1
            self.image = self.images[self.frame_id]

        # movement
        if self.scene.app.jumped:
            self.jump_sound.play()
            self.rect.y -= 20
            self._speed = 0
        else:
            self._speed += self.gravity
            self.rect.y += self._speed
