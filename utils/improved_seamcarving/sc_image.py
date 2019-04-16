from seamcarving import seam_carving
import cv2

in_filename = './assets/bench3.png'
out_filename = './results/bench3_result.png'
X = cv2.imread(in_filename)

width_change = 10
height_change = 0

img = seam_carving(X, width_change, height_change, False)
cv2.imwrite(out_filename, img)