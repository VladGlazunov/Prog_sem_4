import numpy as np
import cv2
import math
import pytesseract

color_red = (0, 0, 255)
color_green = (0, 255, 0)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if ret:
        # Our operations on the frame come here
        working_frame = frame.copy()

        gray = cv2.cvtColor(working_frame, cv2.COLOR_HSV2BGR)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)
        invert_frame = cv2.Canny(gray, 75, 100)

        # Cropping for Main_Frame
        # crop_y_1, crop_x_1 = 300, 300
        # crop_y_2, crop_x_2 = 700, 700
        # crop_filter = invert_frame[crop_y_1:crop_y_2, crop_x_1:crop_x_2]

        # Нахождение контуров по краям
        cont, hierarchy = cv2.findContours(invert_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
                cv2.drawContours(frame, [coord_sq], 0, color_red, 3)
                # Построение рамки
                cv2.rectangle(frame, (x, y), (x + w, y + h), color_green, thickness=3)

                # Распознавание текста (scale у каждого свой)
                h_0, w_0 = extra_frame.shape[:2]
                rotation_matrix = cv2.getRotationMatrix2D(center, main_angle, 1)
                rotated = cv2.warpAffine(extra_frame, rotation_matrix, (w_0, h_0))
                text = pytesseract.image_to_string(rotated, lang="eng", config="--oem 3 --psm 6")
                print(text)
                # cv2.imshow('test', rotated)
                # cv2.waitKey()

                # Вывод значения угла и текста
                cv2.putText(frame, "%d" % int(main_angle) + text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            color_green, 2)

        # Финальный вывод
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()