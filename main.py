import cv2 as cv
from vision import GetVideo, Text
import time


video_stream = GetVideo().start()
ocr = Text().start(video_stream)
time.sleep(.5)
while True:
    pressed_key = cv.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        video_stream.stop()
        ocr.stop()
        break

    cv.imshow("test", video_stream.frame)
    cv.imshow("testw", ocr.altROI)
    cv.imshow("teste", ocr.fpmROI)
