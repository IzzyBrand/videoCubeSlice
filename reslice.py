import cv2
import numpy as np
import sys
import os
from matplotlib import pyplot as plt

# get a name for the video
video_filename = sys.argv[1]
out_filename = 'warped_' + video_filename

# delete the old exported vid if it already exists
if os.path.isfile(out_filename):
    answer = input("{} exists. Do you want to replace it? [y/n]\t")
    if answer.lower() == 'y': os.remove(out_filename)
    else: sys.exit(0)

# calculate the scale for the output video.
scale = 0.25
w = int(1920 * scale)
h = int(1080 * scale)
d = 250 # this is the number of frames that get stored in our "cube"

# cube stores a bunch of video frames. we slice through it
cube = np.zeros([h, d, w, 3], dtype=np.uint8)

# start the video input and output
cap = cv2.VideoCapture(video_filename)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('warped_' + video_filename, -1, 30, (w,h))
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 800,800)

i = 0 # time index
start_exporting = False # we don't want to start exporting until we've filled the cube with frames

# indices for slicing into the cube (in width and height)
x, y = np.meshgrid(np.arange(w), np.arange(h))

while(cap.isOpened()):
    ret, frame = cap.read() # read a video frame
    if not ret: break

    # put it into the cube at layer i. this is basically a circular buffer
    cube[:, i%d] = cv2.resize(frame, dsize=(w, h), interpolation=cv2.INTER_CUBIC)
    i += 1

    # check when we've written every frame of the cube to start exporting
    if not start_exporting and i%d == 0:
        print("Time dimension full. Begin export.")
        start_exporting = True

    if start_exporting:

        # parabolic
        # t = ((x/w*2 - 1)**2 + (y/h*2 - 1)**2)*100 + 1

        # cone
        wh = max(w,h)
        t = np.sqrt(((x - w/2)/wh*2)**2 + ((y-h/2)/wh*2)**2) * d * 0.9 + 1

        # angled slice
        # t = (x)/(w) * (i-d)/(630-d) * d

        # spinning angled slice
        # t = np.sqrt((x/w*2 - 1)**2 + (y/h*2 - 1)**2) * np.sin(np.arctan2(y/h*2 - 1, x/w*2 - 1) + i/d * np.pi * 2) * 100 + 100

        # slice the cube at indices x,y,t
        cube_slice = cube[y, (t+i).astype(int)%d, x]

        # display and save the slice
        out.write(cube_slice)
        cv2.imshow('frame', cube_slice)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

print("Saved {} out of {} frames".format(i-d, i))