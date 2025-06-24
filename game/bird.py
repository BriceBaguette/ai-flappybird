import pygame as pg

class Bird():
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.velocity = 0
        self.jump_strength = -10
        self.sprite_path =  "assets/images/bird.png"
        self.image = pg.transform.scale(pg.image.load(self.sprite_path).convert_alpha(), (self.width, self.height))

    def jump(self):
        self.velocity = self.jump_strength

    def update(self, screen_height: int):
        
        if self.y + self.height < screen_height or  self.velocity < 0:
            self.velocity += self.gravity
            if self.y + self.height + self.velocity >= screen_height:
                self.velocity = 0
                self.y = screen_height - self.height
            self.y += self.velocity

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, (self.x, self.y))