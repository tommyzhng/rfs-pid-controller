import cv2 as cv
from vision import GetVideo, Text
import time

video_stream = GetVideo().start()
ocr = Text().start(video_stream)
while True:
    # Quit condition:
    pressed_key = cv.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        video_stream.stop()
        ocr.stop()
        break
    cv.imshow("test", video_stream.frame)