# Requirements

The object detector is capturing the window of the game in LINUX env, therefore changement need to be done with pygetwindow in windows

# Progress step

- Build flappy bird game in python :white_check_mark:
- Generate dataset by playing the game :white_check_mark:
- Train yolo :white_check_mark:
- Window capture by external program and object detector :white_check_mark:
- Tracker and paralelize the detection to optimize real-time app :x:
- Build InApp RL model 🔲
- Use this architecture in external app combine with computer vision 🔲

# Results

When combining detector with tracker to optimize the speed of inference, we never conclude to good results since the tracking is extremely unaccurate on the bird, since it is a small object moving fast.
When combining detector with tracker to optimize inference speed, we observed poor tracking performance on the bird. The object is small and moves fast, making accurate tracking difficult.

[🎥 Tracking + Detection Result (MP4)](./ai-bot/output_track_detect.mp4)

As a result, we reduced the capture rate to 20 FPS (1 frame every 3 from our 60 FPS game) to maintain better accuracy.

[🎥 Detection Only Result (MP4)](./ai-bot/output_detect.mp4)
