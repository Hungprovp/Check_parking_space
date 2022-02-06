import cv2
import numpy as np
import cvzone
import pickle

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

width, height = 107, 48

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace(imgPro):

    spaceCount = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y: y + height, x: x + width]
        # cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y + height - 10), scale=1, offset=0, thickness=1, colorR=(0, 0, 255))
        if count < 800:
            color = (0, 255, 0)
            thickness = 5
            spaceCount += 1
        else:

            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness=thickness)

    cvzone.putTextRect(img, f'Free: {spaceCount}/{len(posList)}', (100,50), scale=3, offset=15, thickness=5, colorR=(0, 255, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # cv2.imshow('ImageThresh', imgThreshold)
    # cv2.imshow('ImageBlur', imgBlur)
    cv2.imshow('Image', img)
    # cv2.imshow('ImageMedian', imgMedian)
    # cv2.imshow('ImageDilate', imgDilate)
    cv2.waitKey(1)

    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
