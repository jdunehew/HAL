#!/usr/bin/env python

# HAL Intro
# Author - Jeff Dunehew
# 2018


import RPi.GPIO as GPIO
import time
import os
import datetime
import PyCam as PyCam1
import pictureHandler as pictureHandler1
import pygame
from random import *

#stuff for LED fade
LedPin = 7

#setup for eye light
GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
GPIO.output(LedPin, GPIO.LOW)  # Set pin to low(0V)
p = GPIO.PWM(LedPin, 1000)     # set Frequece to 1KHz
p.start(0)

#setup for arcade buttons
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #green button
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #red button
GPIO.setup(15,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #blue button
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #yellow button
prev_input15 = 0
prev_input16 = 0

terminateHAL = 0



def lightBreath(howmanytimes):
#function to fade LED
	loopynumber = 0
	while loopynumber < howmanytimes:
		for dc in range(0, 101, 5):   # Increase duty cycle: 0~100
        	        p.ChangeDutyCycle(dc) # Change duty cycle
                	time.sleep(0.05)
		for dc in range(100, -1, -5): # Decrease duty cycle: 100~0
                	p.ChangeDutyCycle(dc)
               	 	time.sleep(0.05)
		loopynumber=loopynumber+1
	loopynumber = 0
	return

def playGame():
	#function to play number guessing game with user
	#NOTE!!! There may be an issue with prev_input variable from the yes/no. Need to use different variable possibly
	randomnumber = randint(1,5)
	os.system("espeak -ven+f3 -k5 -s150  'Loading game algorythm now'")
	time.sleep(0.5)
	os.system("espeak 'I am sorry I have not received that function yet. Please ask again later.'")
	time.sleep(0.05)
	pygame.mixer.init()
	pygame.mixer.music.load("enjoyable_game.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
        	continue

	lightBreath(2)

	return

def takePicture():
	#function to handle picture taking
	os.system("espeak -ven+f3 -k5 -s150  'Loading picture algorythm now'")
	#Picture stuff now
	timenow = datetime.datetime.now()
	picturefilename = "/home/pi/Pictures/HAL10K/" + str(datetime.datetime.month) + str(datetime.datetime.day) + str(datetime.datetime.year) + str(datetime.datetime.hour) + ":" + str(datetime.datetime.minute) + ".jpg"
	picturefilename = "/home/pi/Pictures/HAL10K/" + "{date:%m-%d-%Y %H:%M}".format(date=datetime.datetime.now()) + ".jpg"
	PyCam1.snapshot(picturefilename)
	pictureHandler1.sendText("8324332405", "Jeff", picturefilename)
	return

def questionsFromHAL():
	#function containing HAL's Questions
	#last question will shut down HAL if user answers YES

	#First Question - Would you like to take a picture
	os.system("espeak 'Would you like to take a picture? Please select green for yes, or red for no'")
	questionOneResult = yesNO()
	if (questionOneResult == 1):
		takePicture()
	else:
		os.system("espeak 'Sorry you do not want a picture today'")

	#Second Question - Would you like to play a game
	os.system("espeak 'Would you like to play a game'")
	questionTwoResult = yesNO()
	if (questionTwoResult == 1):
                playGame()
        else:
                os.system("espeak 'Sorry you do not want to play a game today'")

	#Third Question - Would you like to shut down
	os.system("espeak 'Would you like me to shut down now?'")
	questionThreeResult = yesNO()
	if (questionThreeResult == 1):
		os.system("espeak -ven+f3 -k5 -s150 'You have selected to shut down hal ten thousand now'")
		global terminateHAL
		terminateHAL=1
	else:
		os.system("espeak -ven+f3 -k5 -s150  'Restarting Question Algorythm'")
	return

def yesNO():
	#HAL is going to ask several yes or no questions so need this function to reduce code
	result = 1 #set a default value (of yes)
	os.system("espeak -ven+f3 -k5 -s150  'loading yes no algorythm'")
	#define yesno button var
	prev_input11 = 0
	prev_input13 = 0

	yesnoEndVariable = 0
	sleeptime = 0.03

	looponce=0 #Have to use this because while loop will run once. Keeps it from going inside the if statements.

	#handle green button
	while (yesnoEndVariable==0):
		input11 = GPIO.input(11)
		if ((not prev_input11) and input11 and looponce==1):
			#code for yes
			os.system("espeak -ven+f3 -k5 -s150 'You selected yes'")
			result = 1
			yesnoEndVariable=1
		#update prev_input
		prev_input11 = input11	#slight pause to wait
		time.sleep(sleeptime)

		#handle red button
		input13 = GPIO.input(13)
		if ((not prev_input13) and input13 and looponce==1):
			#code for no
			os.system("espeak -ven+f3 -k5 -s150 'You selected no'")
			result = 0
			yesnoEndVariable=1
		#update prev_input
		prev_input13 = input13
		#slight pause to wait
		looponce=1
		time.sleep(sleeptime)
	return result

#make the eye light up - since it's the most iconic part other than voice
lightBreath(1)

#Play a wav file from the movie 2001- make sure it's in same dir as this program or add file path below
pygame.mixer.init()
pygame.mixer.music.load("hal_9000.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue

lightBreath(2)

pygame.mixer.init()
pygame.mixer.music.load("good_evening.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue

lightBreath(2)


os.system("espeak 'Hello, I am Hal ten thousand. Welcome to C O S C 2 3 2 5. Computer Organization and Architecture'")
lightBreath(1)
time.sleep(.5)
os.system("espeak 'your class is taught by Professor Pamela Betts'")
lightBreath(2)
time.sleep(.5)


while(terminateHAL==0):
	questionsFromHAL()


pygame.mixer.init()
pygame.mixer.music.load("goodbye.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue

lightBreath(2)

os.system("sudo shutdown now")

#HAL turn on
#HAL introduce
#HAL ask for picture
#HAL ask for play game
#HAL ask to turn off or repeat

