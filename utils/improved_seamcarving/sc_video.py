import numpy as np
import cv2
from seamcarving import seam_carving


def save_video(frames, width, height, fps, video_name):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
    for i in range(frames.shape[0]):
        video.write(frames[i, :, :, :])

    cv2.destroyAllWindows()
    video.release()


width_change = -80
height_change = 0
# counting_frames = 10
in_filename = './assets/golf.mov'
out_filename = './results/golf_retarget_all.mp4'
cap = cv2.VideoCapture(in_filename)

frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(
    cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# frames_count = frames_count if counting_frames is None else counting_frames

frames_count = int(frames_count)
fps = int(fps)
width = int(width)
height = int(height)


print 'Video size: ' + str(width) + '*' + str(height)
print 'Frame count: ' + str(frames_count)
print 'New size: ' + str(width+width_change) + '*' + str(height+height_change)

video = np.empty((frames_count, height, width, 3))

i = 0
while cap.isOpened() and i < frames_count:
    ret, X = cap.read()
    if not ret:
        break
    video[i] = X
    i += 1

# start = 10
# step = 8
# out_slice_name = './results/slices/golf_slice_'
# j = 1
# for i in xrange(start, frames_count, step):
#     print 'Frames: ' + str(i) + ':' + str(i+step)
#     temp = video[i:i+step]
#     result = seam_carving(temp, width_change, height_change, False)
#     result = np.clip(result, 0, 255).astype(np.uint8)
#     save_video(result, width+width_change,
#             height+height_change, fps, out_slice_name + str(j) + '.mp4')
#     j = j + 1

result = seam_carving(video, width_change, height_change, False)

result = np.clip(result, 0, 255).astype(np.uint8)
save_video(result, width+width_change,
           height+height_change, fps, out_filename)

cap.release()

print 'Finished! Output file is: ' + out_filename
