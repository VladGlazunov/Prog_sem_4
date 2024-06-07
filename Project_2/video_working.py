import numpy
import numpy as np
import cv2


def Video_working(text):
    cap = cv2.VideoCapture(text)

    if cap.isOpened() == False:
        print('Error opening video stream or file')

    count_frames = 0 # defenetly 175
    repeat = 0
    NonBlackPix = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            count_frames += 1
            #Первоначальная обработка кадра (для video_1)
            working_frame = cv2.resize(frame.copy(), (640, 360))

            gray = cv2.cvtColor(working_frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (9, 9), 0)

            #Crop Filter for Video_1
            crop_filter = gray[40:340, 255:555]
            # crop_filter = gray

            invert_frame = cv2.Canny(crop_filter, 75, 75)

            #Расчет необходимого кадра
            count_black = cv2.countNonZero(invert_frame)
            if count_black > NonBlackPix:
                NonBlackPix = count_black
                final_frame = frame
                final_invert = invert_frame
                #cv2.imshow('Frame', invert_frame)
                #cv2.imshow('Frame', frame)
        else:
            repeat += 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        #кнопа "q" для отсановки видео
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elif repeat > 0:
            cv2.imwrite('Main_Frame.jpg', final_frame)

            # cv2.imwrite('Invert_frame.jpg', final_invert)
            # print(final_invert)
            break
    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     url = "videos/video_2024-05-19_15-28-12.mp4" # input()
#     Video_working('Videos/Video_1.mp4')