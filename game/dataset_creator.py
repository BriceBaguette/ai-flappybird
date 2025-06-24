import pygame as pg
from pipe import Pipe
import os
import uuid

class DatasetCreator:
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Main repository directory
        self.dataset_path = os.path.join(base_dir, "datasets", self.dataset_name)
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)
            os.makedirs(os.path.join(self.dataset_path, "images"))
            os.makedirs(os.path.join(self.dataset_path, "labels"))

    def save_dataset(self, bird_position: tuple, pipes: list[Pipe], screen: pg.surface):
        """Generate data for YOLO format and save it to random file names."""
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        data = []
        # Calculate bounding box for the bird
        bird_x, bird_y = bird_position
        bird_width, bird_height = 34, 24
        bird_bbox = [
            (bird_x + bird_width/2) / screen_width,
            (bird_y + bird_height/2) / screen_height,
            bird_width / screen_width,
            bird_height / screen_height
        ]
        # Append the data in YOLO format
        data.append(f"0 {bird_bbox[0]} {bird_bbox[1]} {bird_bbox[2]} {bird_bbox[3]}\n")

        for pipe in pipes:

            # Calculate bounding box for the top pipe
            pipe_x = pipe.x
            pipe_height = pipe.height
            pipe_width = pipe.width
            pipe_bbox = [
                (pipe_x + pipe_width/2) / screen_width,
                (pipe_height/2) / screen_height,
                pipe_width / screen_width,
                pipe_height / screen_height
            ]
            # Append the data in YOLO format  
            data.append(f"1 {pipe_bbox[0]} {pipe_bbox[1]} {pipe_bbox[2]} {pipe_bbox[3]}\n")

            # Calculate bounding box for the bottom pipe
            bottom_pipe_y = pipe_height + pipe.gap
            bottom_pipe_bbox = [
                (pipe_x + pipe_width/2) / screen_width,
                (screen_height + bottom_pipe_y) / (2 * screen_height),
                pipe_width / screen_width,
                (screen_height - bottom_pipe_y) / screen_height
            ]
            # Append the data in YOLO format
            data.append(f"1 {bottom_pipe_bbox[0]} {bottom_pipe_bbox[1]} {bottom_pipe_bbox[2]} {bottom_pipe_bbox[3]}\n")

        # Save the data to a file
        random_filename = uuid.uuid4()
        with open(f"{self.dataset_path}/labels/{random_filename}.txt", 'w') as f:
            f.writelines(data) 
        pg.image.save(screen, f"{self.dataset_path}/images/{random_filename}.png")
    