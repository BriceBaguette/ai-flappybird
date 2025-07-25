# Requirements

The object detector is capturing the window of the game in LINUX env, therefore changement need to be done with pygetwindow in windows

# Progress step

- Build flappy bird game in python :white_check_mark:
- Generate dataset by playing the game :white_check_mark:
- Train yolo :white_check_mark:
- Window capture by external program and object detector :white_check_mark:
- Tracker and paralelize the detection to optimize real-time app :red_cross:
- Build InApp RL model
- Use this architecture in external app combine with computer vision

# Results

When combining detector with tracker to optimize the speed of inference, we never conclude to good results since the tracking is extremely unaccurate on the bird, since it is a small object moving fast.

<video width="144" height="256" controls>
  <source src="./ai-bot/output_track_detect.mp4" type="video/mp4">
</video>

Therefore, we will reduce the speed of capture to 20 FPS, meaning we get the positing every 3 frames since our game is at 60 FPS to have accurate results.

<video width="144" height="256" controls>
  <source src="./ai-bot/output_detect.mp4" type="video/mp4">
</video>
