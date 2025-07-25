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
        self.bird_bbox: tuple
        self.pipe_bbox_list: list[tuple] = []
        self.bird_tracker: cv.TrackerVit = None
        self.pipe_multi_tracker: list[cv.TrackerVit] = []
        self.tracker_net = cv.dnn.readNetFromONNX("backbone.onnx")

    def detect_objects(self, image: cv.Mat) -> list:
        """Detect objects in the given image."""
        results = self.model(image)
        self.pipe_bbox_list = []
        self.pipe_multi_tracker = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = int(box.cls[0])
                if label == 0 and box.conf > 0.8:
                    self.bird_bbox = (x1, y1, x2, y2)
                    #if self.bird_tracker == None:
                    #    self.bird_tracker = cv.TrackerVit.create(self.tracker_net)
                    #    self.bird_tracker.init(image, utils.xyxy_to_xywh(self.bird_bbox))
                elif label == 1 and box.conf > 0.8:
                    self.pipe_bbox_list.append(( x1, y1, x2, y2))
                    #pipe_tracker = cv.TrackerVit.create(self.tracker_net)
                    #pipe_tracker.init(image, utils.xyxy_to_xywh(( x1, y1, x2, y2)))
                    #self.pipe_multi_tracker.append(pipe_tracker)
    
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
        x1, y1, x2, y2 = self.bird_bbox
        print(self.bird_bbox)
        cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[0], 2)
        return image
    
    def allocate_video(self, image: cv.Mat, output_path: str):
        """Allocate a video writer for saving the output video."""
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(output_path, fourcc, 20.0, (int(image.shape[1]), int(image.shape[0])))
        return out

    def make_video(self, image:cv.Mat, out: cv.VideoWriter, fps: float):
        """Process a video file and save the output with detections."""
        if out is None:
            raise ValueError("Output video writer is not initialized.")
        if image is None:
            raise ValueError("Invalid image provided for processing.")

        frame_with_detections = self.draw_detections(image)

        # Ajout du temps sur l'image
        text = f"{fps:.2f} FPS"
        cv.putText(
            frame_with_detections,
            text,
            (10, 30),  # position (x, y)
            cv.FONT_HERSHEY_SIMPLEX,
            0.8,       # taille de police
            (0, 255, 0),  # couleur (vert)
            2,         # épaisseur du texte
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
