import cv2
import numpy as np


def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if action == 'NO_FILTER':
        filtered = img
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif width > 200:
            k = (25, 25)
        else:
            k = (10, 10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == "BINARY":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        filtered = cv2.bitwise_not(img)
    elif action == 'FACE_DETECTION':
        img = image
        facecascade = cv2.CascadeClassifier(
            "static/haarcascade_frontalface_default.xml")
        eyecascade = cv2.CascadeClassifier("static/haarcascade_eye.xml")
        imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(imggray, 1.6, 4)
        for (x, y, w, h) in faces:

            cv2.circle(img, (x+w//2, y+h//2), h//2+20, (0, 185, 0), 5)
            roi_gray = imggray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eyecascade.detectMultiScale(roi_gray, 1.1, 4)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex + ew, ey + eh), (0, 0, 255), 2)

        filtered = img

    elif action == 'CLASSIFICATION':
        img = image
        classFile = 'static/classifier/coco.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        configpath = 'static/classifier/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightspath = 'static/classifier/frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightspath, configpath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        classids, confs, bbox = net.detect(img, confThreshold=0.52)

        if len(classids) != 0:

            for classid, confidence, box in zip(classids.flatten(), confs.flatten(), bbox):
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=3)
                cv2.putText(img, classNames[classid - 1].upper(), (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_TRIPLEX, 1,
                            (255, 255, 0), 2)
        filtered = img
    elif action == 'SKETCHED':
        img = image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(img_gray)
        img_smoothing = cv2.GaussianBlur(
            img_invert, (21, 21), sigmaX=0, sigmaY=0)

        def dodgeV2(x, y):
            return cv2.divide(x, 255 - y, scale=256)
        final_img = dodgeV2(img_gray, img_smoothing)
        filtered = final_img
    elif action == "SHAPE":

        def getcontours(img):
            contours, hierarchy = cv2.findContours(
                img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                area = cv2.contourArea(cnt)

                if area > 500:
                    cv2.drawContours(imgcontour, cnt, -1, (255, 0, 0), 3)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

                    objcolor = len(approx)
                    x, y, w, h = cv2.boundingRect(approx)
                    if objcolor == 3:
                        objectType = "Tri"
                    elif objcolor == 4:
                        aspratio = w/float(h)
                        if aspratio > 0.95 and aspratio < 1.05:
                            objectType = "squre"
                        else:
                            objectType = "rectangle"
                    elif objcolor == 5:
                        objectType = "pentagon"
                    elif objcolor == 6:
                        objectType = "hexagon"
                    elif objcolor == 7:
                        objectType = "heptagon"
                    elif objcolor == 8:
                        objectType = "octagon"
                    elif objcolor > 10:
                        objectType = "circle"
                    else:
                        objectType = "polygon"
                    cv2.rectangle(imgcontour, (x, y),
                                  (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(imgcontour, objectType, (x+(w//2)-5, y+(h//2)-10),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
        img = image
        imgcontour = img.copy()
        imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgblur = cv2.GaussianBlur(imggray, (7, 7), 1)
        imgcanny = cv2.Canny(imgblur, 50, 50)
        getcontours(imgcanny)
        filtered = imgcontour
        getcontours(imgcanny)
        filtered = imgcontour
    elif action == "DOCUMENT":
        filtered = get_flatten_document(image)
    else:
        filtered = np.zeros((512, 512, 3), np.uint8)
        cv2.putText(filtered, "No Action", (100, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 100), 10)
    return filtered


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 130)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres


def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    # cv2.drawContours(imgContour, biggest, -1, (0, 0, 255), 20)
    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew


def getWarp(img, biggest, widthImg, heightImg):

    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32(
        [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[10:imgOutput.shape[0] -
                           10, 10:imgOutput.shape[1] - 10]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))

    return imgCropped


def get_flatten_document(img):
    widthImg = img.shape[0]
    heightImg = img.shape[1]
    img = cv2.resize(img, (widthImg, heightImg))
    img = cv2.detailEnhance(img, 10, 0.25)
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    imgContour = img.copy()
    cv2.drawContours(imgContour, biggest, -1, (0, 0, 255), 20)
    if biggest.size != 0:
        imgWraped = getWarp(img, biggest, widthImg, heightImg)

    else:
        imgWraped = img

    return cv2.resize(imgWraped, (heightImg, widthImg))
