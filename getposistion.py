import cv2
import numpy as np


def find_largest_rectangle(contours):
    max_area = 0
    largest_rectangle = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > max_area:
            max_area = area
            largest_rectangle = contour
    return largest_rectangle


cap = cv2.VideoCapture(0)
position = None  # 创建一个变量用于存储矩形轮廓的坐标

while True:
    ret, frame = cap.read()

    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 60, 60)

    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    largest_rectangle = find_largest_rectangle(contours)

    if largest_rectangle is not None:
        x, y, w, h = cv2.boundingRect(largest_rectangle)
        position = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]  # 将矩形四个顶点的坐标赋值给 position

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        perimeter = cv2.arcLength(largest_rectangle, True)
        approx = cv2.approxPolyDP(largest_rectangle, 0.02 * perimeter, True)
        CornerNum = len(approx)

        if CornerNum == 4:
            if w == h:
                objType = "Square"
            else:
                objType = "Rectangle"
        else:
            objType = "N"

        cv2.putText(frame, "Coordinates: x={}, y={}, w={}, h={}".format(x, y, w, h), (10, 30), cv2.FONT_HERSHEY_COMPLEX,
                    0.6, (0, 0, 0), 1)

        # 在屏幕上显示矩形四个顶点的坐标
        cv2.putText(frame, "Top Left: {}".format(position[0]), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(frame, "Top Right: {}".format(position[1]), (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(frame, "Bottom Right: {}".format(position[2]), (10, 120), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0),
                    1)
        cv2.putText(frame, "Bottom Left: {}".format(position[3]), (10, 150), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0),
                    1)

        top_left = position[0]
        top_right = position[1]
        bottom_right = position[2]
        bottom_left = position[3]

    cv2.imshow("capture", frame)
    tempfile = open("temp.txt", "w")
    tempstr = str(top_left[0]) + ' ' + str(top_left[1]) + ' ' + str(top_right[0]) + ' ' + str(top_right[1]) + ' ' + str(
        bottom_left[0]) + ' ' + str(bottom_left[1]) + ' ' + str(bottom_right[0]) + ' ' + str(bottom_right[1])

    tempfile.write(tempstr)
    tempfile.close()


    def tempread():
        tempfiles = open("temp.txt", "r")
        templine = tempfiles.readline()
        tempsplit = templine.split(" ")
        for i in range(0, len(tempsplit)):
            tempsplit[i] = int(tempsplit[i])
        # print(tempsplit)
        return tempsplit
        tempfiles.close()


    tempread()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
