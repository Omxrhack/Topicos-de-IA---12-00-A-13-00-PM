import cv2
import numpy as np

def detect_plate_region(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = keypoints[0] if len(keypoints) == 2 else keypoints[1]

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)

        if len(approx) == 4:
            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [approx], 0, 255, -1)

            x, y = np.where(mask == 255)
            if len(x) == 0 or len(y) == 0:
                continue

            topX, topY = np.min(x), np.min(y)
            bottomX, bottomY = np.max(x), np.max(y)

            cropped = gray[topX:bottomX+1, topY:bottomY+1]
            return cropped

    return gray
