import math
import numpy
import pytesseract
import numpy as np
import cv2

from video_working import Video_working
color_red = (0, 0, 255)
color_green = (0, 255, 0)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

file_name = str(input("File's name.mp4 ", ))

# Впишите одну из нижеперечисленных строк
# Videos/Video_1.mp4
# Videos/Video_2.mp4
# Videos/Video_3.mp4

Video_working(file_name)

main_frame = cv2.imread('Main_Frame.jpg')
working_frame = main_frame.copy()

# For Main_Frame: COLOR_BGR2YCrCb
# For Main_Frame_2-3: COLOR_BGR2HSV
contrast = cv2.cvtColor(working_frame, cv2.COLOR_BGR2YCrCb)
contrast = cv2.GaussianBlur(contrast, (9, 9), 0)

# Cropping for Main_Frame
crop_y_1, crop_x_1 = 200, 600
crop_y_2, crop_x_2 = 480, 900

# Cropping for Main_Frame_2
# crop_y_1, crop_x_1 = 400, 400
# crop_y_2, crop_x_2 = 700, 900

# Cropping for Main_Frame_3
# crop_y_1, crop_x_1 = 500, 300
# crop_y_2, crop_x_2 = 800, 900

main_frame = main_frame[crop_y_1:crop_y_2, crop_x_1:crop_x_2]
crop_filter = contrast[crop_y_1:crop_y_2, crop_x_1:crop_x_2]

invert_frame = cv2.Canny(crop_filter, 35, 180)

# Нахождение контуров по краям
cont, hierarchy = cv2.findContours(invert_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(main_frame, cont, 3, color_red, thickness=2)

x, y, w, h = 0, 0, 0, 0
count = 0

for c in cont:
    x, y, w, h = cv2.boundingRect(c)
    # something = cv2.arcLength(c, True)
    # approx = cv2.approxPolyDP(c, cv2.arcLength(c, True), True)

    # Поиск угла наклона
    rect = cv2.minAreaRect(c)
    coord_sq = cv2.boxPoints(rect)  # Поиск координат вершин прямоугольника
    coord_sq = np.intp(coord_sq)  # Округление значений координат
    S_area = int(rect[1][0] * rect[1][1])
    center = (int(rect[0][0]), int(rect[1][0]))

    # Вектора сторон прямоугольника
    vect_1 = np.intp((coord_sq[1][0] - coord_sq[0][0], coord_sq[1][1] - coord_sq[0][1]))
    vect_2 = np.intp((coord_sq[2][0] - coord_sq[1][0], coord_sq[2][1] - coord_sq[1][1]))

    # Вектор горизонта
    vect_horz = (1, 0)

    used_vect = vect_1
    if cv2.norm(vect_2) > cv2.norm(vect_1):
        used_vect = vect_2

    # Угол наклона в градусах
    main_angle = (180 / math.pi) * (vect_horz[0] * used_vect[0] + vect_horz[1] * used_vect[1]) / (
            cv2.norm(vect_horz) * cv2.norm(used_vect))


    if S_area > 6500:
        extra_frame = invert_frame.copy()

        # Выделение исходного контура
        cv2.drawContours(main_frame, [coord_sq], 0, color_red, 3)
        # Построение рамки
        cv2.rectangle(main_frame, (x, y), (x + w, y + h), color_green, thickness=3)

        # Распознавание текста (scale у каждого свой)
        h_0, w_0 = extra_frame.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D(center, main_angle,2.7)
        rotated = cv2.warpAffine(extra_frame, rotation_matrix, (w_0, h_0))
        text = pytesseract.image_to_string(rotated, lang="eng", config="--oem 3 --psm 6")
        print(text)

        # cv2.imshow('test', rotated)
        # cv2.waitKey()

        # Вывод значения угла и текста
        cv2.putText(main_frame, "%d" % int(main_angle) + text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color_green, 2)


cv2.imshow('Frame', main_frame)
cv2.waitKey()
cv2.imwrite('Final_Frame_1.jpg', main_frame)
cv2.destroyAllWindows()
