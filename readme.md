# Flappy Bird AI with Computer Vision

## 🛠 Requirements

This project captures and processes the **Flappy Bird game window on Windows** using an object detection pipeline.  
Due to the lack of easy screen capture tools on Linux and since developing a custom recorder is out of scope, **all development is done on Windows**.

## 🚧 Project Progress

- ✅ Build Flappy Bird clone in Python
- ✅ Generate a dataset by playing the game
- ✅ Train a YOLO-based object detector
- ✅ Capture game window using an external process and apply object detection
- ✅ Add object tracking and parallelize detection for better real-time performance
- 🔲 Build an in-app Reinforcement Learning (RL) model for comparison
- ✅ Integrate vision model with an external control agent
- 🔲 Increase game speed to test model limits under more difficult conditions

---

## 📈 Results

### 🎯 Object Detection Only

The system captures the game window in real-time and detects the bird and pipes using a YOLOv5 model.  
Detection is handled in a separate process to allow smooth inference and gameplay monitoring.

▶️ [Watch detection-only demo (YouTube Short)](https://youtube.com/shorts/6ywJ87_Ch_0)

---

### 🧠 Detection + Tracking

To speed up inference, tracking was added to reduce the need for continuous detection. However, results showed that **tracking failed on the bird**, due to its small size and rapid movement.

▶️ [Watch detection + tracking demo (YouTube Short)](https://youtube.com/shorts/AXUniph27dM)

**Conclusion:** Tracking was too inaccurate. For training the AI agent, we rely only on detection, which runs at ~25–30 FPS, while the game runs at 60 FPS.

---

### 🤖 Learning to Play with NEAT

We used **NEAT (NeuroEvolution of Augmenting Topologies)**, a genetic algorithm, to evolve a neural network that learns to play the game based on computer vision inputs.

- After **6 generations**, the AI achieved a **score of 100**.
- The input features are extracted from the object detector and fed to the neural network to decide when to flap.

<img src="NEAT_BEST_CV.gif" alt="Best NEAT Agent Playing" width="288">
