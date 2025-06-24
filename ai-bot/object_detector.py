from ultralytics import YOLO
import cv2 as cv

CLASS2COLOR = {
    0: (255, 0, 0),    # Blue
    1: (0, 255, 0),    # Green
}

class ObjectDetector:
    def __init__(self, model_path: str):
        """Initialize the object detector with a YOLO model."""
        self.model = YOLO(model_path)

    def detect_objects(self, image: cv.Mat) -> list:
        """Detect objects in the given image."""
        results = self.model(image)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = int(box.cls[0])
                confidence = float(box.conf[0])
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'label': label,
                    'confidence': confidence
                })
        return detections
    
    def draw_detections(self, image: cv.Mat, detections: list) -> cv.Mat:
        """Draw bounding boxes and labels on the image."""
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            label = detection['label']
            cv.rectangle(image, (x1, y1), (x2, y2),CLASS2COLOR[label], 2)
        return image
    
    def allocate_video(self, image: cv.Mat, output_path: str):
        """Allocate a video writer for saving the output video."""
        fourcc = cv.VideoWriter_fourcc(*'MPEG')
        out = cv.VideoWriter(output_path, fourcc, 60.0, (int(image.shape[1]), int(image.shape[0])))
        return out

    def make_video(self, image:cv.Mat, out: cv.VideoWriter):
        """Process a video file and save the output with detections."""
        if out is None:
            raise ValueError("Output video writer is not initialized.")
        if image is None or not isinstance(image, cv.Mat):
            raise ValueError("Invalid image provided for processing.")
        detections = self.detect_objects(image)
        frame_with_detections = self.draw_detections(image, detections)
        out.write(frame_with_detections)

    def release_video(self, out: cv.VideoWriter):
        """Release the video writer."""
        if out is not None:
            out.release()
        else:
            raise ValueError("Output video writer is not initialized.")
