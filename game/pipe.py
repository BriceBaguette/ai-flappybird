import pygame as pg

class Pipe:
    def __init__(self, x: int, width: int, height: int, speed: int = 3, gap: int = 175):
        """Initialize the pipe with position and size."""
        self.x = x
        self.speed = speed
        self.width = width
        self.height = height
        self.gap = gap
        self.passed = False
        self.sprite_path = "assets/images/pipe-green.png"
        self.image = pg.image.load(self.sprite_path).convert_alpha()

    
    def isRemovable(self):
        """Check if the pipe is off-screen and can be removed."""
        return self.x < -self.width

    def update(self):
        self.x -= self.speed

    def draw(self, screen: pg.Surface):
        """Draw the pipe on the screen."""
        top_pipe = pg.transform.rotate(self.image, 180)
        screen.blit(top_pipe, (self.x, self.height - self.image.get_height()))
        screen.blit(self.image, (self.x, self.height + self.gap))

 