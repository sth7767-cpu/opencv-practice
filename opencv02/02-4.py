import cv2

img = cv2.imread('lena.jpg')
b,g,r = cv2.split(img)

#채널 병합
cv2.merge((r,g,b))


cv2.imshow('blue',b)
cv2.imshow('green',g)
cv2.imshow('red',r)
cv2.waitKey(0)
cv2.destroyAllWindows()
