import pyautogui
from threading import Thread
from time import sleep, time
from PID.controllerPID import PID

class Control:
    def __init__(self):
        self.pid = PID()
        self.pidON = False
        self.stopped = False
        self.yAxis = 0

    def ControlCenter(self, altitude, fpm, time):
        self.yAxis = self.pid.compute(altitude, fpm, time)
        self.joystick(self.yAxis)
        pass


    def start(self, ocr):
        self.ocr = ocr
        Thread(target=self.callControls, args=()).start()
        return self
    def callControls(self):
        sleep(1)
        while not self.stopped:
            self.ControlCenter(int(self.ocr.alt), int(self.ocr.fpm), float(self.ocr.time))
            sleep(0.01)
    def stop(self):
        self.stopped = True

    ##########   MOUSE OUTPUTS   ##########
    def activateAP(self):
        ##Autopilot
        pyautogui.moveTo(1980, 350)
        pyautogui.click()
        pyautogui.moveTo(2170, 340)
        pyautogui.click()
        pyautogui.moveTo(2170, 450)
        pyautogui.click()

        ##Flaps and Spoilers
        pyautogui.moveTo(3740, 510)
        pyautogui.dragRel(0, 1000, 0.4)
        pyautogui.moveTo(3740, 710)
        pyautogui.dragRel(0, -200, 0.2)
    
        ##Gear and Brakes
        pyautogui.moveTo(3740, 650)
        pyautogui.click()
        pyautogui.moveTo(3740, 810)
        pyautogui.click()

    def deactivateAP(self):
        pyautogui.moveTo(2170, 340)
        pyautogui.click()
        pyautogui.moveTo(2300, 340)
        pyautogui.click()

    def joystick(self, dy):
        if self.pidON == False:
            pyautogui.moveTo(3500,770)
            pyautogui.mouseDown()
            self.pidON = True
        
        dy = 770+(dy*145)
        pyautogui.moveTo(3500, dy)
        pass

    def temp(self, altitude):
        if altitude == 0:
            start = time()
            while (time() - start) <= 3:
                pass

        if altitude >= 1000:
            self.activateAP()

        if altitude <= 125:
            self.deactivateAP()
    


    
    
        
