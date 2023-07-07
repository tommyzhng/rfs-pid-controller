import cv2 as cv
from threading import Thread
import pytesseract
import math
import time
import numpy as np
import re

class GetVideo(): #get video from another thread to reduce latency
    def __init__(self) -> None:
        self.stream = cv.VideoCapture(2, cv.CAP_DSHOW)
        self.stream.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        (self.success, self.frame) = self.stream.read() #read the first frame
        self.stopped = False

    def start(self):
        Thread(target=self.getframes, args=()).start() #start a thread to read frames
        return self

    def getframes(self):
        while not self.stopped:
            if not self.success: ##if cant grab frame, then stop the thread
                self.stop()
            else:
                (self.success, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
        self.stream.release()
        cv.destroyAllWindows()

class Text():
    def __init__(self):
        self.stream = None
        self.stopped = False
        self.custom_oem=r'--psm 7 -c tessedit_char_whitelist=-0123456789'

        self.lastalt = None
        self.lastfpm = None

        self.fpm = 0
        self.array = []
        self.offset = 0

        #post processing
        self.pattern = r'^-?\d{1,3}$'

    def altitude(self, frame):
        x,y,width,height = 579, 668, 42-self.offset, 20
        self.altROI = frame[y:y+height,x:x+width]
        self.altROI = self.preprocessing(self.altROI)
        self.alt = pytesseract.image_to_string(self.altROI, lang='digits', config=self.custom_oem)
        #self.alt, self.lastalt = self.print_with_errors(self.alt, self.lastalt, 10)
        self.alt = self.alt.replace("\n",'')
        self.offset = 9 if int(self.alt) <= 100 else 0

        print(f"alt: {self.alt} fpm: {self.fpm}")

    def verticalSpeed(self, frame):
        x,y,width,height = 730, 662, 50, 17
        self.fpmROI = frame[y:y+height,x:x+width]
        self.fpmROI = self.preprocessing(self.fpmROI)
        self.fpm = pytesseract.image_to_string(self.fpmROI, lang='digits',config=self.custom_oem)
        #self.fpm, self.lastfpm = self.print_with_errors(self.fpm, self.lastfpm, 20)
        self.fpm = self.fpm.replace("\n",'')

    def print_with_errors(self, reading, lastReading, measuringAlt=False):
        
        if reading != '':
            reading = int(reading)
            if lastReading == None:
                lastReading = reading
            if abs(lastReading-reading) <= math.sqrt(constant*lastReading) + 5:
                lastReading = reading
            else:
                reading = str(lastReading) + "DUPLICATE"
        else:
            if lastReading != None:
                reading = lastReading
        return str(reading), lastReading
              
    def preprocessing(self,frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        width = int(frame.shape[1] * 20)
        height = int(frame.shape[0] * 20)
        frame = cv.resize(frame, (width, height))
        
        clahe = cv.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8))
        frame = clahe.apply(frame)

        _, frame = cv.threshold(frame, 115, 255, cv.THRESH_BINARY_INV)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        frame = cv.dilate(frame, kernel, iterations=2)
        frame = cv.erode(frame, kernel, iterations=2)

        return frame    
    
    def start(self, video_stream):
        Thread(target=self.get_alt, args=()).start()
        Thread(target=self.get_fpm, args=()).start()
        self.stream = video_stream
        return self

    def get_alt(self):
        while not self.stopped:
            if self.stream is not None:
                frame = self.stream.frame
                self.altitude(frame)
    def get_fpm(self):
        while not self.stopped:
            if self.stream is not None:
                frame = self.stream.frame
                self.verticalSpeed(frame)
    
    def stop(self):
        self.stopped = True



