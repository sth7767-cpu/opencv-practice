import cv2
import numpy as np

# 이미지 읽기
img = cv2.imread('coins.jpg')
if img is None:
    raise FileNotFoundError('coins.jpg 파일을 찾을 수 없습니다.')

src = img.copy()

# 1. 전처리: 그레이스케일 + 블러
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 2. 이진화
# 배경이 밝고 동전이 더 진해서 inverse threshold 사용
_, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)

# 3. 노이즈 제거: Opening + Closing
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

# 4. 윤곽선 검출
contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

coin_count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)

    # 너무 작은 잡음 제거
    if area < 1000:
        continue

    coin_count += 1
    cv2.drawContours(src, [cnt], -1, (0, 255, 0), 2)

# 5. 결과 텍스트 출력
cv2.putText(
    src,
    f'Found {coin_count} coins',
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.imshow('gray', gray)
cv2.imshow('threshold', thresh)
cv2.imshow('morphology', closing)
cv2.imshow('result', src)
cv2.waitKey(0)
cv2.destroyAllWindows()