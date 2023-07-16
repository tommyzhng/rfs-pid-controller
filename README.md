# RFS-AI
Goal: Establish a PID model to land an airplane in the game RFS real flight simulator using only vision from tesseract-OCR

##contents
* [General info](#general-info)
* [Technologies](#technologies)

## General info
This project contains 4 Python scripts that are called when running main.py. Each script had multithreading for different functions to reduce latency and processing delay from the neural networks. 

- vision.py is used to convert an obs virtual camera source video feed into numbers, using tesseract ocr. It obtains the altitude and descent rate readings from the game using a pre-trained number recognition model. 
- control.py is used to establish the pyautogui commands, along with hosting a control center for calling the PID controller.
- control
	
## Technologies
Project is created with:
* Lorem version: 12.3
* Ipsum version: 2.33
* Ament library version: 999
	

https://github.com/tommyzhng/RFS-AI/assets/109367999/d6a82b24-2f2c-4278-b067-9b7da1531a8d

