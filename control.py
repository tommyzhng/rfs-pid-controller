import pyautogui
from threading import Thread
from time import sleep
from PID.controllerPID import PID

class Control:
    def __init__(self):
        self.pid = PID()
        self.pidON = False
        self.stopped = False
        self.yAxis = 0

        self.apOn = False
        self.landed = False
        self.landedTime = 0
        self.dy = None
        self.messageSent = False

    def ControlCenter(self, altitude, fpm, time):
        if altitude >= 1000:
            if not self.apOn:
                self.activateAP()
                self.apOn = True
                return
            return

        if altitude <= 130 and altitude != 0 and not self.landed:
            if self.apOn:
                self.deactivateAP()
                print("Took over controls")
                self.apOn = False
            self.yAxis = self.pid.compute(altitude, fpm, time)
            self.joystick(self.yAxis)
            self.printStatus(altitude)
            return
        
        if altitude == 0 and not self.landed:
            self.landedTime = time
            self.landed = True
            print("Touchdown")

        if 3 <= (time - self.landedTime) <= 3.5:
            pyautogui.mouseUp()
            self.dy = None
            print("Landed...")
            sleep(2)
            print("starting world domination")
            self.pid.graph(self.pid.times, self.pid.positions, self.pid.descentRates)

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

    def printStatus(self,altitude):
        if 50 < altitude <= 100:
            print(f"Preparing to flare")
        if 0 <= altitude <= 50:
            print(f"Flaring: {altitude} feet")
            

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
            pyautogui.moveTo(3450,770)
            pyautogui.mouseDown()
            self.pidON = True
 
        self.dy = 770+(dy*145)
        pyautogui.moveTo(3450, self.dy)


    
    
        
