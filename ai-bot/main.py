import pygetwindow as gw
import mss
import cv2
import numpy as np
import time
import neat
import keyboard
import pyautogui
import pickle
from object_detector import ObjectDetector 
from neat.reporting import StdOutReporter
from neat.statistics import StatisticsReporter

WINDOW_TITLE = "Flappy Bird"
DETECT_FRAME = 3
generation_counter = 1

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
    config_path = "neat-config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    population = neat.Population(config)
    population.add_reporter(StdOutReporter(True))
    stats = StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    # Sauvegarde du genome gagnant
    with open("winner_genome.pkl", "wb") as f:
        pickle.dump(winner, f)

def eval_genomes(genomes, config):
    global generation_counter
    print(f"Waiting for window titled: '{WINDOW_TITLE}'")
    win = None

    # Attente que la fenêtre soit ouverte
    while win is None:
        win = find_window(WINDOW_TITLE)

    print("Window detected.")
    win.activate()
    win.moveTo(900,300)
    if win.isMinimized:
        win.restore()
      
    time.sleep(0.2)  # Laisser le temps à l'OS
    pyautogui.click(win.left + 10, win.top + 10)  # Clic en haut à gauche de la fenêtre
    time.sleep(0.1)    

    object_detector = ObjectDetector("yolo_model.pt")
    
    for genome_id, genome in genomes:
        time.sleep(0.5)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        start = time.time()
        run(win,object_detector=object_detector, net=net, genome_id=genome_id, generation=generation_counter)
        genome.fitness = time.time() - start

    generation_counter += 1
    

def run(win, object_detector: ObjectDetector, net: neat.nn.FeedForwardNetwork, genome_id, generation):
    ready = False
    first_check = False
    alive = True
    
    with mss.mss() as sct:
        # Capture initiale pour initialiser le writer vidéo
        init_frame = capture_window(win, sct)
        out = object_detector.allocate_video(init_frame, "./training/output_detect" + str(generation) +"_" + str(genome_id) + ".mp4")
        neat_info = (generation,genome_id)
        try:
            while alive:
                win = find_window(WINDOW_TITLE)
                if win is None:
                    print("Window closed. Exiting.")
                    break

                if win.isMinimized:
                    print("Window is minimized. Skipping frame.")
                    time.sleep(0.5)
                    continue

                frame = capture_window(win, sct)
                
                start_time = time.time()
                object_detector.detect_objects(frame)
                    
                fps = 1/(time.time() - start_time)    
                # Traitement et enregistrement
                
                out_frame = object_detector.make_video(frame, out, fps, neat_info)
                
                if ready:
                    if object_detector.bird_bbox == None:
                        if first_check:
                            alive = False
                        first_check = True
                        continue
                    else:
                        features = object_detector.get_features()
                        output = net.activate(features)
                        if output[0] > 0.5:
                            keyboard.press_and_release("space")

                # Affichage live (optionnel)
                cv2.imshow("Live Capture", out_frame)
                if cv2.waitKey(1) == ord('q'):
                    print("User quit with 'q'.")
                    break
                
                if ready == False:
                    keyboard.press_and_release("r")
                    print("pressed")
                    ready = True

        finally:
            object_detector.release_video(out)
            cv2.destroyAllWindows()
            print("Video released and windows closed.")

if __name__ == "__main__":
    main()
