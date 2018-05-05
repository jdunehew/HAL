#!/usr/bin/env python

# HAL Intro
# Authors - Jeff Dunehew & Chelsea Handler
# 2018


import RPi.GPIO as GPIO
import time
import os
import datetime
import PyCam as PyCam1
import pictureHandler as pictureHandler1
import pygame
from random import *

GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location

#setup for arcade buttons
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #green button
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #red button
GPIO.setup(15,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #blue button
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)  #yellow button
prev_input15 = 0
prev_input16 = 0

terminateHAL = 0

def playGame():
        #null return
	#Function to play number guessing game with user using side buttons
	#NOTE!!! There may be an issue with prev_input variable from the yes/no. Need to use different variable possibly
	randomnumber = randint(1,4) #Generate a random number 1 <= rnum <= 4
	playerGuess = 0 #Variable that holds the player's guess; an int that represents a button, see chooseButton()
	gameOver = 0 #Control variable for game loop (redundant but makes me feel better)
	allowedGuesses = 3 #Number of guesses the player is allowed per game
	timesGuessed = 0 #Number of times the player has guessed
	os.system("espeak -ven+f3 -k5 -s150  'Loading game algorythm now'")
	time.sleep(0.5)
	#Game Loop
	while (gameOver==0 and (timesGuessed<allowedGuesses)):
            if (timesGuessed==0):
				os.system("espeak 'Guess the correct button. Green, Red, Blue or Yellow. You have 3 attempts. Good Luck.'")
            if (timesGuessed==1):
				os.system("espeak 'Guess the correct button. You have two attempts left'")
            if (timesGuessed==2):
				os.system("espeak 'This is your last try. Good luck!'")
            print ("timesGuessed = " + str(timesGuessed))
            time.sleep(0.05)
            #While the playerGuess hasn't been altered, seek a guess
            while (playerGuess==0):
                playerGuess = chooseButton()
                time.sleep(0.05)
            #Increment timesGuessed variable after playerGuess is altered from 0
            timesGuessed += 1
            #If the player's guess is correct, play "mission complete," break from game loop
            if (playerGuess==randomnumber):
                pygame.mixer.init()
                pygame.mixer.music.load("completed.wav") #http://www.rosswalker.co.uk/movie_sounds/sounds_files_20150201_1096714/2001_and_2010/completed.wav
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
                gameOver=1
                time.sleep(0.05)
                break
            #Incorrect guess block
            else:
                #If player has used up all guesses, play "can't do that dave"
                if (timesGuessed >= allowedGuesses): #Somewhat unfortunate that this condition must be tested each time, but can't think of another way currently
                    pygame.mixer.init()
                    pygame.mixer.music.load("cantdothat.wav") #http://www.rosswalker.co.uk/movie_sounds/sounds_files_20150201_1096714/2001_and_2010/cantdo.wav
                    pygame.mixer.music.play()
                    time.sleep(0.5)
                    while pygame.mixer.music.get_busy() == True:
                        continue
                #Else, player can still play; play "just what do you think you're doing, dave?", reset their guess to 0, restart from top of game loop.
                else:
                    if (gameOver==0):
						pygame.mixer.init()
						pygame.mixer.music.load("dave.wav") #https://2001archive.files.wordpress.com/2015/07/dave.wav
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy() == True:
							continue
						playerGuess = 0
						time.sleep(0.5)

        #Once out of game loop, thank player and exit function
        time.sleep(0.5)
	pygame.mixer.init()
	pygame.mixer.music.load("enjoyable_game.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
        	continue
        time.sleep(0.5)
        os.system("espeak -ven+f3 -k5 -s150 'Leaving game algorithm.'")
	return

def chooseButton():
	result = 1 #set a default value of green
	os.system("espeak -ven+f3 -k5 -s150  'loading button selection algorythm'")
	#define yesno button var
	prev_input11 = 0
	prev_input13 = 0
	prev_input15 = 0
	prev_input16 = 0

	chooseButtonEndVariable = 0
	sleeptime = 0.03

	looponce=0 #Have to use this because while loop will run once. Keeps it from going inside the if statements.

	while (chooseButtonEndVariable==0):
		#handle green button
		input11 = GPIO.input(11)
		if ((not prev_input11) and input11 and looponce==1):
			os.system("espeak -ven+f3 -k5 -s150 'You selected green'")
			result = 1
			chooseButtonEndVariable=1
		#update prev_input
		prev_input11 = input11	#slight pause to wait
		time.sleep(sleeptime)

		#handle red button
		input13 = GPIO.input(13)
		if ((not prev_input13) and input13 and looponce==1):
			os.system("espeak -ven+f3 -k5 -s150 'You selected red'")
			result = 2
			chooseButtonEndVariable=1
		#update prev_input
		prev_input13 = input13
		#slight pause to wait
		time.sleep(sleeptime)
		
		#handle blue button
		input15 = GPIO.input(15)
		if ((not prev_input15) and input15 and looponce==1):
			os.system("espeak -ven+f3 -k5 -s150 'You selected blue'")
			result = 3
			chooseButtonEndVariable=1
		#update prev_input
		prev_input15 = input15	#slight pause to wait
		time.sleep(sleeptime)
		
		#handle blue button
		input16 = GPIO.input(16)
		if ((not prev_input16) and input16 and looponce==1):
			os.system("espeak -ven+f3 -k5 -s150 'You selected yellow'")
			result = 3
			chooseButtonEndVariable=1
		#update prev_input
		prev_input16 = input16	#slight pause to wait
		time.sleep(sleeptime)
		
		looponce=1
	return result

def takePicture():
	#function to handle picture taking
	os.system("espeak -ven+f3 -k5 -s150  'Loading picture algorythm now'")
	#Picture stuff now
	now = datetime.datetime.now()
	picturefilename = "/home/pi/Pictures/HAL10K/" + str(now.month) + str(now.day) + str(now.year) + str(now.hour) + ":" + str(now.minute) + ".jpg"
	PyCam1.snapshot(picturefilename)
	pygame.mixer.init()
	pygame.mixer.music.load("cam.mp3")
	pygame.mixer.music.play()
	os.system("espeak -ven+f3 -k5 -s150  'Attempting to send picture now. Please stand by'")
	while pygame.mixer.music.get_busy() == True:
		continue
	print("Name of file: " + picturefilename)
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


#Play a wav file from the movie 2001- make sure it's in same dir as this program or add file path below
#pygame.mixer.init()
#pygame.mixer.music.load("hal_9000.wav")
#pygame.mixer.music.play()
#while pygame.mixer.music.get_busy() == True:
	#continue

pygame.mixer.init()
pygame.mixer.music.load("2001_theme.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue
time.sleep(.5)

os.system("espeak 'Hello, I am Hal ten thousand. Welcome to C O S C 2 3 2 5. Computer Organization and Architecture'")
time.sleep(.5)
os.system("espeak 'your class is taught by Professor Pamela Betts'")
time.sleep(.5)

while(terminateHAL==0):
	questionsFromHAL()

pygame.mixer.init()
pygame.mixer.music.load("goodbye.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue


os.system("sudo shutdown now")

#HAL turn on
#HAL introduce
#HAL ask for picture
#HAL ask for play game
#HAL ask to turn off or repeat

