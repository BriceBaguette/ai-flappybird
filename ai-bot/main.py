import subprocess
import mss
import numpy as np
import cv2
import time

WINDOW_TITLE = "Flappy Bird"  # Change this

def get_window_geometry(window_title):
    # Get window id using xdotool
    try:
        win_id = subprocess.check_output(["xdotool", "search", "--name", window_title]).decode().strip().split("\n")[0]
    except subprocess.CalledProcessError:
        return None

    # Get window info using xwininfo
    win_info = subprocess.check_output(["xwininfo", "-id", win_id]).decode()

    # Parse position and size
    x = int([line for line in win_info.splitlines() if "Absolute upper-left X" in line][0].split()[-1])
    y = int([line for line in win_info.splitlines() if "Absolute upper-left Y" in line][0].split()[-1])
    width = int([line for line in win_info.splitlines() if "Width:" in line][0].split()[-1])
    height = int([line for line in win_info.splitlines() if "Height:" in line][0].split()[-1])

    return {"top": y, "left": x, "width": width, "height": height}

def capture_window(region):
    with mss.mss() as sct:
        img = np.array(sct.grab(region))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def main():
    print(f"Waiting for window titled: '{WINDOW_TITLE}'")
    region = None
    while region is None:
        region = get_window_geometry(WINDOW_TITLE)
        time.sleep(1)

    print("Window detected.")
    while True:
        region = get_window_geometry(WINDOW_TITLE)
        if region is None:
            print("Window closed. Exiting.")
            break

        frame = capture_window(region)
        cv2.imshow("Capture", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
