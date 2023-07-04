import cv2 as cv
from threading import Thread
import pytesseract
import math
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
        self.custom_oem=r'digits --psm 7 -c tessedit_char_whitelist=0123456789'

        self.lastalt = None

    def start(self, video_stream):
        Thread(target=self.get_text, args=()).start()
        self.stream = video_stream

        return self

    def get_text(self):
        while not self.stopped:
            if self.stream is not None:
                frame = self.stream.frame
                self.altitude(frame)

    def altitude(self, frame):
        x,y,width,height = 0, 677, 60, 18
        self.altROI = frame[y:y+height,x:x+width]
        self.altROI = cv.resize(self.altROI, (0, 0), fx=10, fy=10)
        self.altROI = self.preprocessing(self.altROI)

        self.alt = pytesseract.image_to_string(self.altROI, config=self.custom_oem)
        self.alt, self.lastalt = self.print_with_errors(self.alt, self.lastalt)
        
    
    def print_with_errors(self, var, lastvar):
        if var != '':
            var = int(var)
            if lastvar == None:
                lastvar = var
            if abs(lastvar-var) <= math.sqrt(10*lastvar) + 5:
                lastvar = var
            else:
                var = lastvar
        else:
            if lastvar != None:
                var = lastvar
        return var, lastvar
              
    def preprocessing(self,frame):
        frame = cv.threshold(frame, 178, 255, cv.THRESH_BINARY)[1]
        rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
        frame = cv.dilate(frame, rect_kernel, iterations = 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return frame    
    
    def stop(self):
        self.stopped = True


