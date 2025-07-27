import pygame as pg
from bird import Bird
from typing import List
from pipe import Pipe
import random

class FlappyBird:
    """A class representing the Flappy Bird game."""
    
    def __init__(self):
        """Initialize the game."""
        self.bird: Bird = None
        self.pipes: List[Pipe] = []  # Start with one pipe
        self.pipe_gap = 175
        self.score = 0
        self.background = pg.image.load("assets/images/background-day.png").convert()
        self.isStarted = False

    def jump(self):
        """Make the bird jump."""
        self.bird.jump()
    
    def start(self):
        """Start the game"""
        if not self.isStarted:
            self.isStarted = True
            self.bird = Bird(50, 200, 34, 24)
            self.score = 0

    def update(self, screen_width: int, screen_height: int):
        """Run the game loop."""
        self.bird.update(screen_height=screen_height)
        # Update pipes
        for pipe in self.pipes:
            pipe.update()

        if len(self.pipes) == 0 or (self.pipes and self.pipes[-1].x < screen_width - 250):
            # Add a new pipe if the last one is far enough or if there are no pipes
            new_pipe_height = random.randint(int(screen_height/8), int(screen_height * 7/8) - self.pipe_gap)
            new_pipe = Pipe(screen_width, 52, new_pipe_height, speed=3, gap=self.pipe_gap)
            self.pipes.append(new_pipe)

        if len(self.pipes) > 0 and self.pipes[0].isRemovable():
            self.pipes.pop(0)  # Remove the first pipe if it's off-screen
        
        # Check for collisions with pipes
        for pipe in self.pipes:
            if (self.bird.x + self.bird.width > pipe.x and
                self.bird.x < pipe.x + pipe.width and
                (self.bird.y < pipe.height or self.bird.y + self.bird.height > pipe.height + pipe.gap)):
                self.set_over()
                break
        # Check if the bird has passed a pipe
        first_pipe = self.pipes[0] if self.pipes else None
        if first_pipe and not first_pipe.passed:
            pipe = first_pipe
            # Check if the bird has passed the pipe
            if not pipe.passed and self.bird.x > pipe.x + pipe.width:
                pipe.passed = True
                self.score += 1
                
    def set_over(self):
        self.isStarted = False
        self.bird = None
        self.pipes = []

    def draw(self, screen: pg.Surface):
        """Draw the game elements on the screen."""
        screen.blit(self.background, (0, 0))
        if self.isStarted:
            self.bird.draw(screen)
            for pipe in self.pipes:
                pipe.draw(screen)
            # Draw the score
            font = pg.font.Font(None, 36)
            score_text = font.render(str(self.score), True, (255, 255, 255))
            screen.blit(score_text, (screen.get_width()/2 - score_text.get_width()/2, 10))   
        else:
            score_font = pg.font.Font(None, 54)
            score_text = score_font.render(str(self.score), True, (255, 255, 255))
            
            text_font = pg.font.Font(None, 40)
            text = text_font.render("Press 'R' to start", True, (255, 255, 255))
            
            screen.blit(score_text, (screen.get_width()/2 - score_text.get_width()/2, screen.get_height()/2 - 2* score_text.get_height()/2))
            screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 + 8))   
        