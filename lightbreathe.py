
import RPi.GPIO as GPIO
import time


#stuff for LED fade
LedPin = 7

#setup for eye light
GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
GPIO.output(LedPin, GPIO.LOW)  # Set pin to low(0V)
p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
p.start(0)

while True:
	time.sleep(0.03)
	for dc in range(0, 101, 5):   # Increase duty cycle: 0~100
        	        p.ChangeDutyCycle(dc) # Change duty cycle
                	time.sleep(0.05)
	for dc in range(100, -1, -5): # Decrease duty cycle: 100~0
                	p.ChangeDutyCycle(dc)
               	 	time.sleep(0.1)



	
#def lightBreath(howmanytimes):
##function to fade LED
	#loopynumber = 0
	#while loopynumber < howmanytimes:
		#for dc in range(0, 101, 5):   # Increase duty cycle: 0~100
        	        #p.ChangeDutyCycle(dc) # Change duty cycle
                	#time.sleep(0.05)
		#for dc in range(100, -1, -5): # Decrease duty cycle: 100~0
                	#p.ChangeDutyCycle(dc)
               	 	#time.sleep(0.05)
		#loopynumber=loopynumber+1
	#loopynumber = 0
	#return
