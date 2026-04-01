import cv2
import sys


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_RBUTTONDBLCLK:
        print("오른쪽 버튼 더블 클릭:", x, y)


# 이미지 불러오기
img = cv2.imread('../opencv04/lena.jpg')

if img is None:
    print("이미지를 찾을 수 없습니다.")
    sys.exit()

cv2.imshow('Lena Window', img)
cv2.setMouseCallback('Lena Window', mouse_callback)

# 키 입력 대기
cv2.waitKey(0)
cv2.destroyAllWindows()