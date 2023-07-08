import pyautogui
from threading import Thread
from time import sleep, time
import os

class Train:
    def __init__(self):
        self.controls = ControlMethods()

        self.apActivated = False
        self.stopped = False

    def startTraining(self, altitude, fpm, speed):
        if altitude == 0:
            start = time()
            while (time() - start) <= 3:
                pass
            if altitude == 0:
                self.controls.restart()

        if altitude >= 1000:
            if self.apActivated == False:
                self.controls.activateAP()
                self.apActivated = True

        if altitude <= 125:
            if self.apActivated == True:
                self.controls.deactivateAP()
                self.apActivated = False
                return
    
            if self.apActivated == False:
                #train model here
                pass

    def createRL():
        #logPath = os.path.join('trainingRL', 'logs')
        pass

        
    def start(self, ocr):
        self.ocr = ocr
        Thread(target=self.callTraining, args=()).start()
        return self
    def callTraining(self):
        while not self.stopped:
            self.startTraining(int(self.ocr.alt), int(self.ocr.fpm), int(self.ocr.spd))
            sleep(0.01)
    def stop(self):
        self.stopped = True

class ControlMethods():
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

    def restart(self):
        #pause, and reset
        pyautogui.moveTo(3775, 1040)
        pyautogui.click()
        sleep(0.5)
        pyautogui.moveTo(3350, 600)
        pyautogui.click()
        pyautogui.moveTo(3775, 1040)
        pyautogui.click()
        sleep(7)
        #click calibration prompt
        pyautogui.moveTo(3350, 600)
        pyautogui.click()
        sleep(2)



    
    
        
