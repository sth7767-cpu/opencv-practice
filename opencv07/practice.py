import cv2
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)

points = [deque(maxlen=1024)]
color_index = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)]
color_names = ["BLUE", "GREEN", "RED", "YELLOW", "PURPLE"]

kernel = np.ones((5, 5), np.uint8)

paint = np.zeros((480, 640, 3), dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 0])
    upper = np.array([180, 255, 60])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = None

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 500:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 255, 255), -1)
                points[-1].appendleft(center)
    else:
        points.append(deque(maxlen=1024))

    for i in range(len(points)):
        for j in range(1, len(points[i])):
            if points[i][j - 1] is None or points[i][j] is None:
                continue
            cv2.line(frame, points[i][j - 1], points[i][j], colors[color_index], 5)
            cv2.line(paint, points[i][j - 1], points[i][j], colors[color_index], 5)

    cv2.rectangle(frame, (0, 0), (640, 60), (50, 50, 50), -1)
    cv2.putText(frame, "C : CLEAR", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "P : COLOR CHANGE", (180, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, color_names[color_index], (500, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[color_index], 2)

    result = cv2.add(frame, paint)

    cv2.imshow("Air Canvas", result)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break
    elif key == ord('c') or key == ord('C'):
        paint = np.zeros((480, 640, 3), dtype=np.uint8)
        points = [deque(maxlen=1024)]
    elif key == ord('p') or key == ord('P'):
        color_index = (color_index + 1) % len(colors)

cap.release()
cv2.destroyAllWindows()