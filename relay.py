import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

relay_pinA = 11
relay_pinB = 12
GPIO.setup(relay_pinA,GPIO.OUT)
GPIO.setup(relay_pinB,GPIO.OUT)

def winner(team,stat):
	if team == A:
		if stat == win:
			GPIO.output(relay_pinA,HIGH)
		else:
			GPIO.output(relay_pinA,LOW)
	elif team == B:
		if stat == win:
			GPIO.output(relay_pinB,HIGH)
		else:
			GPIO.output(relay_pinB,LOW)
	else:
		GPIO.output(relay_pinA,LOW)
		GPIO.output(relay_pinB,LOW)
		
	
