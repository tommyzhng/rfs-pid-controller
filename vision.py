import cv2 as cv
from threading import Thread
import pytesseract
import re
from time import time


class GetVideo(): #get video from another thread to reduce latency
    def __init__(self):
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
        self.alt = 1000
        self.fpm = 0
        self.spd = 200

        #preprocess
        self.custom_oem=r'--psm 7 -c tessedit_char_whitelist=-0123456789'
        self.lastalt = self.alt
        self.lastfpm = self.fpm
        self.lastspd = None
        self.offset = 0

        #post processing
        self.pattern = r'^-?\d{1,4}$'
        self.startTime = time()
        self.time = 0

    def altitude(self, frame):
        x,y,width,height = 579, 668, 42-self.offset, 20
        self.altROI = frame[y:y+height,x:x+width]
        self.altROI = self.preprocessing(self.altROI)
        self.altRAW = pytesseract.image_to_string(self.altROI, lang='digits',config=self.custom_oem)
        self.alt, self.lastalt = self.postprocess(self.altRAW, self.lastalt)
        self.offset = 9 if int(self.alt) <= 105 else 0
        self.time = time()-self.startTime
        #print(f"alt: {self.alt}")

    def verticalSpeed(self, frame):
        x,y,width,height = 240, 424, 50, 17
        self.fpmROI = frame[y:y+height,x:x+width]
        self.fpmROI = self.preprocessing(self.fpmROI)
        self.fpmRAW = pytesseract.image_to_string(self.fpmROI, lang='digits',config=self.custom_oem)
        self.fpm, self.lastfpm = self.postprocess(self.fpmRAW, self.lastfpm)
        #print(f"fpm: {self.fpm}")
    
    #########     Post/Preprocessing     #########
    def preprocessing(self,frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        width = int(frame.shape[1])
        height = int(frame.shape[0])
        frame = cv.resize(frame, (width*10, height*10))
        
        clahe = cv.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8))
        frame = clahe.apply(frame)

        _, frame = cv.threshold(frame, 115, 255, cv.THRESH_BINARY_INV)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        frame = cv.dilate(frame, kernel, iterations=2)
        frame = cv.erode(frame, kernel, iterations=2)

        return frame
        
    def postprocess(self, curReading, lastReading):
            curReading = curReading.replace("\n",'')
            if curReading == '':
                curReading = lastReading
            
            if not re.match(self.pattern, str(curReading)):          #if the reading doesnt match pattern, assign cur reading to last
                curReading = lastReading
                return curReading, lastReading
            
            try:
                curReading = int(curReading)
                lastReading = curReading
            except ValueError:
                curReading = lastReading
            return curReading, lastReading
              

    #########     Multithreading     #########
    def start(self, video_stream):
        Thread(target=self.get_alt, args=()).start()
        Thread(target=self.get_fpm, args=()).start()
        self.stream = video_stream
        return self

    def get_alt(self):
        while not self.stopped:
            if self.stream is not None:
                self.altitude(self.stream.frame)

    def get_fpm(self):
        while not self.stopped:
            if self.stream is not None:
                self.verticalSpeed(self.stream.frame)

    def stop(self):
        self.stopped = True


