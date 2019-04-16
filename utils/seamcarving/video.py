import numpy as np
import cv2
from seam_carving import SeamCarver

filename = 'ratatouille1.mov'

# counting_frames = 2
cap = cv2.VideoCapture(filename)

frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(
    cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# frames_count = frames_count if counting_frames is None else counting_frames

print(frames_count)
print(fps)
print(height)
print(width)

new_height = 256
new_width = 480

# video = np.empty((int(frames_count), int(new_height), int(new_width), 3))

i = 0
while cap.isOpened() and i < frames_count:
    print(i)
    ret, X = cap.read()
    if not ret:
        break
    cv2.imwrite('tmp.png', X.astype(np.uint8))
    obj = SeamCarver('tmp.png', new_height, new_width)
    obj.save_result('./images/res_' + "%02d" %i + '.png', )
    # video[i] = obj.get_img()
    i += 1

# video_name = 'video.mp4'
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# result = cv2.VideoWriter(video_name, fourcc, fps, (new_width, new_height))
# for i in range(video.shape[0]):
#     result.write(video[i,:,:,:])

# cv2.destroyAllWindows()
# result.release()
