# Requirements

The object detector is capturing the window of the game in WINDOWS env, since it's not available in LINUX to capture the screen easily. Since that's not part of the project to implement a windows recorder in LINUX, I rather pursue the development in WINDOWS.

# Progress step

- Build flappy bird game in python :white_check_mark:
- Generate dataset by playing the game :white_check_mark:
- Train yolo :white_check_mark:
- Window capture by external program and object detector :white_check_mark:
- Tracker and paralelize the detection to optimize real-time app :white_check_mark:
- Build InApp RL model for comparaisons 🔲
- Use this architecture in external app combine with computer vision :white_check_mark:
- Speed up game tick speed and make game harder to see limitations 🔲

# Results

When combining detector with tracker to optimize the speed of inference, we never conclude to good results since the tracking is extremely unaccurate on the bird, since it is a small object moving fast.
When combining detector with tracker to optimize inference speed, we observed poor tracking performance on the bird. The object is small and moves fast, making accurate tracking difficult.

[🎥 Tracking + Detection Result (MP4)](https://youtube.com/shorts/AXUniph27dM)

As a result, we reduced the capture rate to 20 FPS (1 frame every 3 from our 60 FPS game) to maintain better accuracy.

[🎥 Detection Only Result (MP4)](https://youtube.com/shorts/6ywJ87_Ch_0)

When using NEAT which is a genetic algorithm to learn to play with CV, we achieve a score of 100 after 6 generations.

<img src="NEAT_BEST_CV.gif" alt="Final Result" width="288">
