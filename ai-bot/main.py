import pygetwindow as gw
import mss
import cv2
import numpy as np
import time
from object_detector import ObjectDetector  # Assure-toi que ce fichier est bien importable

WINDOW_TITLE = "Flappy Bird"  # Titre exact de la fenêtre

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
    cv2.imwrite("debug_frame.png", img)
    
    return img

def main():
    print(f"Waiting for window titled: '{WINDOW_TITLE}'")
    win = None

    # Attente que la fenêtre soit ouverte
    while win is None:
        win = find_window(WINDOW_TITLE)

    print("Window detected.")
    win.activate()

    object_detector = ObjectDetector("yolo_model.pt")

    with mss.mss() as sct:
        # Capture initiale pour initialiser le writer vidéo
        init_frame = capture_window(win, sct)
        cv2.imshow("Live Capture", cv2.imread("debug_frame.png"))
        out = object_detector.allocate_video(init_frame, "output_detector.mp4")
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
                # Traitement et enregistrement
                out_frame = object_detector.make_video(frame, out)

                # Affichage live (optionnel)
                cv2.imshow("Live Capture", out_frame)
                if cv2.waitKey(1) == ord('q'):
                    print("User quit with 'q'.")
                    break

        finally:
            object_detector.release_video(out)
            cv2.destroyAllWindows()
            print("Video released and windows closed.")

if __name__ == "__main__":
    main()
