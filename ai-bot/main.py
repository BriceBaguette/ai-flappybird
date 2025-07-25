import pygetwindow as gw
import mss
import cv2
import numpy as np
import time
from object_detector import ObjectDetector 

WINDOW_TITLE = "Flappy Bird"
DETECT_FRAME = 3

def find_window(title) -> gw.Window: 
    windows = gw.getWindowsWithTitle(title)
    return windows[0] if windows else None

def capture_window(win: gw.Window, sct):
    # Récupérer les dimensions de la fenêtre
    left, top, width, height = win.left, win.top, win.width, win.height
    bbox = {"top": top, "left": left, "width": width, "height": height}

    # Capture de l'écran
    screenshot = sct.grab(bbox)
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    return img

def main():
    print(f"Waiting for window titled: '{WINDOW_TITLE}'")
    win = None
    frame_count = 0

    # Attente que la fenêtre soit ouverte
    while win is None:
        win = find_window(WINDOW_TITLE)

    print("Window detected.")
    win.activate()

    object_detector = ObjectDetector("yolo_model.pt")

    with mss.mss() as sct:
        # Capture initiale pour initialiser le writer vidéo
        init_frame = capture_window(win, sct)
        out = object_detector.allocate_video(init_frame, "output_detect.mp4")
        try:
            while True:
                win = find_window(WINDOW_TITLE)
                if win is None:
                    print("Window closed. Exiting.")
                    break

                if win.isMinimized:
                    print("Window is minimized. Skipping frame.")
                    time.sleep(0.5)
                    continue

                frame = capture_window(win, sct)
                
                #Object tracking
                start_time = time.time()
                if frame_count == 0:
                    object_detector.detect_objects(frame)
                    #frame_count = DETECT_FRAME
                #else:
                #    object_detector.track_objects(frame)
                #    frame_count -= 1
                    
                fps = 1/(time.time() - start_time)    
                # Traitement et enregistrement
                
                out_frame = object_detector.make_video(frame, out, fps)

                # Affichage live (optionnel)
                cv2.imshow("Live Capture", out_frame)
                if cv2.waitKey(1) == ord('q'):
                    print("User quit with 'q'.")
                    break
                if fps > 20:
                    time.sleep(1/20 - 1/fps)

        finally:
            object_detector.release_video(out)
            cv2.destroyAllWindows()
            print("Video released and windows closed.")

if __name__ == "__main__":
    main()
