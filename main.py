import cv2 as cv
from vision import GetVideo, Text
from control import Control
import time

video_stream = GetVideo().start()
ocr = Text().start(video_stream)
control = Control().start(ocr)

time.sleep(.5)
while True:
    if control.dy != None:
        video_stream.frame = cv.circle(video_stream.frame, (1020, int(control.dy*0.666667)), 50, (0,0,255), 4)
    
    cv.imshow("main", video_stream.frame)
    cv.imshow("altitude (ft)", ocr.altROI)
    cv.imshow("descent rate (fpm)", ocr.fpmROI)
    #print(f"            altitude: {ocr.alt} ft               descent rate: {ocr.fpm} fpm")

    pressed_key = cv.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        video_stream.stop()
        ocr.stop()
        control.stop()
        break
