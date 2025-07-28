from ultralytics import YOLO
import cv2 as cv
import numpy as np
import utils

CLASS2COLOR = {
    0: (255, 0, 0),    # Blue
    1: (0, 255, 0),    # Green
}

class ObjectDetector:
    def __init__(self, model_path: str):
        """Initialize the object detector with a YOLO model."""
        self.model = YOLO(model_path)
        self.bird_bbox: tuple = None
        self.previous_bird_bbox: tuple = None
        self.pipe_bbox_list: list[tuple] = []
        # self.bird_tracker: cv.TrackerVit = None
        # self.pipe_multi_tracker: list[cv.TrackerVit] = []
        self.tracker_net = cv.dnn.readNetFromONNX("backbone.onnx")

    def detect_objects(self, image: cv.Mat) -> list:
        """Detect objects in the given image."""
        results = self.model(image)
        self.pipe_bbox_list = []
        # self.pipe_multi_tracker = []
        self.bird_bbox = None
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = int(box.cls[0])
                if label == 0 and box.conf > 0.8:
                    if self.previous_bird_bbox is not None:
                        self.previous_bird_bbox = self.bird_bbox
                    self.bird_bbox = (x1, y1, x2, y2)
                    if self.previous_bird_bbox == None:
                        self.previous_bird_bbox = self.bird_bbox
                    #if self.bird_tracker == None:
                    #    self.bird_tracker = cv.TrackerVit.create(self.tracker_net)
                    #    self.bird_tracker.init(image, utils.xyxy_to_xywh(self.bird_bbox))
                elif label == 1 and box.conf > 0.8:
                    self.pipe_bbox_list.append(( x1, y1, x2, y2))
                    #pipe_tracker = cv.TrackerVit.create(self.tracker_net)
                    #pipe_tracker.init(image, utils.xyxy_to_xywh(( x1, y1, x2, y2)))
                    #self.pipe_multi_tracker.append(pipe_tracker)
    
    def get_closest_pipes(self) -> list[tuple]:
        bird_x2 = self.bird_bbox[2] 
        pipes_sorted = sorted(self.pipe_bbox_list, key=lambda pipe: pipe[0])
        pipes_ahead = [pipe for pipe in pipes_sorted if pipe[0] > bird_x2]
        return pipes_ahead[:2]
    
    def get_features(self) -> list[float]:
        features = []

        pipes = self.get_closest_pipes()
        if len(pipes) < 2:
            return [self.bird_bbox[1], 0, 0, 0, 0]
        if pipes[0][1] > pipes[1][1]:
            pipes.reverse()
            
        features = [self.bird_bbox[1],
                    abs(self.bird_bbox[1] - pipes[0][3]),
                    abs(self.bird_bbox[0] - pipes[0][0]),
                    self.previous_bird_bbox[1] - self.bird_bbox[1]
                    ]

        return features

    
    def track_objects(self, image: cv.Mat):
        _, self.bird_bbox = self.bird_tracker.update(image)
        self.bird_bbox = utils.xywh_to_xyxy(self.bird_bbox)
        for idx, tracker in enumerate(self.pipe_multi_tracker):
            _, self.pipe_bbox_list[idx] = tracker.update(image)
            self.pipe_bbox_list[idx] = utils.xywh_to_xyxy(self.pipe_bbox_list[idx])
    
    def draw_detections(self, image: cv.Mat) -> cv.Mat:
        """Draw bounding boxes and labels on the image."""
        for pipe_bbox in self.pipe_bbox_list:
            x1, y1, x2, y2 = pipe_bbox
            cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[1], 2)
        if not self.bird_bbox == None:
            x1, y1, x2, y2 = self.bird_bbox
            cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[0], 2)
        return image
    
    def allocate_video(self, image: cv.Mat, output_path: str):
        """Allocate a video writer for saving the output video."""
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(output_path, fourcc, 30.0, (int(image.shape[1]), int(image.shape[0])))
        return out

    def make_video(self, image: cv.Mat, out: cv.VideoWriter, fps: float, neat_info: tuple):
        """Process a video frame and save the output with detections and NEAT info."""
        if out is None:
            raise ValueError("Output video writer is not initialized.")
        if image is None:
            raise ValueError("Invalid image provided for processing.")

        frame_with_detections = self.draw_detections(image)

        # Ajout du FPS
        fps_text = f"{fps:.2f} FPS"
        cv.putText(
            frame_with_detections,
            fps_text,
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv.LINE_AA
        )

        # Ajout des infos NEAT : génération et genome_id
        generation, genome_id = neat_info
        neat_text = f"Gen {generation} - Genome {genome_id}"
        cv.putText(
            frame_with_detections,
            neat_text,
            (10, 60),  # légèrement plus bas que le FPS
            cv.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),  # jaune
            2,
            cv.LINE_AA
        )

        out.write(frame_with_detections)
        return frame_with_detections


    def release_video(self, out: cv.VideoWriter):
        """Release the video writer."""
        if out is not None:
            out.release()
        else:
            raise ValueError("Output video writer is not initialized.")
