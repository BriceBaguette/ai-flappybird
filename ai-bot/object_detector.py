from ultralytics import YOLO
import cv2 as cv
import time

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

    def detect_objects(self, image: cv.Mat) -> list:
        """Detect objects in the given image."""
        results = self.model(image)
        self.pipe_bbox_list = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = int(box.cls[0])
                if label == 0 and box.conf > 0.8:
                    print(box)
                    self.bird_bbox = (x1, y1, x2, y2)
                elif label == 1 and box.conf > 0.8:
                    self.pipe_bbox_list.append(( x1, y1, x2, y2))
    
    def track_objects(self, image: cv.Mat, trackers):
        return
    
    def draw_detections(self, image: cv.Mat) -> cv.Mat:
        """Draw bounding boxes and labels on the image."""
        for pipe_bbox in self.pipe_bbox_list:
            x1, y1, x2, y2 = pipe_bbox
            cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[1], 2)
        x1, y1, x2, y2 = self.bird_bbox
        print(self.bird_bbox)
        print(x1,y1,x2,y2)
        cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[0], 2)
        return image
    
    def allocate_video(self, image: cv.Mat, output_path: str):
        """Allocate a video writer for saving the output video."""
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(output_path, fourcc, 15.0, (int(image.shape[1]), int(image.shape[0])))
        return out

    def make_video(self, image:cv.Mat, out: cv.VideoWriter):
        """Process a video file and save the output with detections."""
        if out is None:
            raise ValueError("Output video writer is not initialized.")
        if image is None:
            raise ValueError("Invalid image provided for processing.")
        start_time = time.time()
        
        self.detect_objects(image)
        fps = 1/(time.time() - start_time) 

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
