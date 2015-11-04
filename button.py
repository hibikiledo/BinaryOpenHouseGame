import RPi.GPIO as GPIO
from time import sleep

buttonA_1 = 13
buttonA_2 = 37
buttonA_4 = 16
buttonA_sub = 18

buttonB_1 = 19
buttonB_2 = 21
buttonB_4 = 22
buttonB_sub = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonA_1,GPIO.IN)
GPIO.setup(buttonA_2,GPIO.IN)
GPIO.setup(buttonA_4,GPIO.IN)
GPIO.setup(buttonA_sub,GPIO.IN)
GPIO.setup(buttonB_1,GPIO.IN)
GPIO.setup(buttonB_2,GPIO.IN)
GPIO.setup(buttonB_4,GPIO.IN)
GPIO.setup(buttonB_sub,GPIO.IN)


def button_state():
	A1 = GPIO.input(buttonA_1) == True
	A2 = GPIO.input(buttonA_2) == True
	A4 = GPIO.input(buttonA_4) == True
	Asub = GPIO.input(buttonA_sub) == True
	B1 = GPIO.input(buttonB_1) == True
	B2 = GPIO.input(buttonB_2) == True
	B4 = GPIO.input(buttonB_4) == True
	Bsub = GPIO.input(buttonB_sub) == True
	sleep(0.3)
	return (A1,A2,A4,Asub,B1,B2,B4,Bsub)
