import cv2 as cv
from vision import GetVideo, Text
from control import Control
import time

video_stream = GetVideo().start()
ocr = Text().start(video_stream)
control = Control().start(ocr)

time.sleep(.5)
while True:
    cv.imshow("main", video_stream.frame)
    cv.imshow("altitude (ft)", ocr.altROI)
    cv.imshow("descent rate (fpm)", ocr.fpmROI)
    #print(f"alt: {ocr.alt} fpm: {ocr.fpm}, spd: {ocr.spd}")

    pressed_key = cv.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        video_stream.stop()
        ocr.stop()
        control.stop()
        break
