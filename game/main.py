import sys
import pygame as pg
from game import FlappyBird
from dataset_creator import DatasetCreator

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
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game.jump()

        game.update(screen_width=screen.get_width(), screen_height=screen.get_height())
        game.draw(screen)
        
        pg.display.update()
        
        clock.tick(60)

        if game.game_over:
            print(f"Game Over! Your score: {game.score}")
            running = False
        elif create_dataset:
            # Save dataset for YOLO format
            bird_position = (game.bird.x, game.bird.y)
            dataset_creator.save_dataset(bird_position, game.pipes, screen)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

        screen.fill((0, 0, 0))
        font = pg.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        pg.display.update()

if __name__ == "__main__":
    main()