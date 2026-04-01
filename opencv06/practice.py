import cv2

img = cv2.imread("people.jpg")
if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

# 작은 이미지면 확대
img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 대비 향상
gray = cv2.equalizeHist(gray)

# 분류기 로드
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 얼굴 검출
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.05,
    minNeighbors=3,
    minSize=(30, 30)
)

print("검출된 얼굴 수:", len(faces))

# 검출된 얼굴마다 사각형 그리기
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()