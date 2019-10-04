# videoCubeSlice

Messing with the temporal and spatial dimensions in video playback.

Imagine stacking all the frames of a video (2D arrays) into a rectangular prism (a 3D array). A normal playback of the video displays sequential slices of the rectangular prism along the time axis. Imagine instead slice the prism diagonal along the time axis and a spatial axis -- the video playback will be warped in space and time.

## Requirements

 - numpy
 - python3.7
 - opencv4 (I used [this tutorial](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) to install on mac)

## How to use

python3 reslice.py [input_video]