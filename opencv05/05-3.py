import cv2
import numpy as np

img = cv2.imread('morphology.jpg', cv2.IMREAD_GRAYSCALE)

kernel = np.ones((5, 5), np.uint8)

# 침식
erosion = cv2.erode(img, kernel, iterations=1)

# 팽창
dilation = cv2.dilate(img, kernel, iterations=1)

# 닫힘
result = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.imshow('erosion', erosion)
cv2.imshow('dilation', dilation)
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()