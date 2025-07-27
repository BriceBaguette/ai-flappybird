import sys
import pygame as pg
from game import FlappyBird
from dataset_creator import DatasetCreator
import time

def main():
    """Main function to run the Flappy Bird game."""
    pg.init()
    pg.display.set_caption("Flappy Bird")
    screen = pg.display.set_mode((288, 512))
    clock = pg.time.Clock()
    game = FlappyBird()
    dataset_creator = DatasetCreator("flappy_bird_dataset") 
    create_dataset = "-c" in sys.argv
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_SPACE and game.isStarted:
                    game.jump()
                if event.key == pg.K_r:
                    game.start()
                    continue
        if game.isStarted:
            game.update(screen_width=screen.get_width(), screen_height=screen.get_height())
        game.draw(screen)
        
        pg.display.update()
        
        clock.tick(30)
        if create_dataset:
            # Save dataset for YOLO format
            bird_position = (game.bird.x, game.bird.y)
            dataset_creator.save_dataset(bird_position, game.pipes, screen)

if __name__ == "__main__":
    main()