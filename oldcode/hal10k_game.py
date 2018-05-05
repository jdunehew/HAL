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
	while (gameOver==0 && (timesGuessed<=allowedGuesses)):
            os.system("espeak 'Guess the correct button.'")
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
                gameOver==1
                time.sleep(0.05)
                break
            #Incorrect guess block
            else:
                #If player has used up all guesses, play "can't do that dave"
                if (timesGuessed >= allowedGuesses): #Somewhat unfortunate that this condition must be tested each time, but can't think of another way currently
                    pygame.mixer.init()
                    pygame.mixer.music.load("cantdo.wav") #http://www.rosswalker.co.uk/movie_sounds/sounds_files_20150201_1096714/2001_and_2010/cantdo.wav
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue
                #Else, player can still play; play "just what do you think you're doing, dave?", reset their guess to 0, restart from top of game loop.
                else:
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
        os.system("espeak -ven+f3 -k5 -s150 'Leaving game algorithm.'")
	lightBreath(2)

return

def chooseButton():
        #Returns int chosenButton
        #Function that returns an int that signifies which button was pressed
        os.system("espeak -ven+f3 -k5 -s150 'Loading button choosing algorithm'")
        pin11 = 1 #green button int val
	pin13 = 2 #red button int val
	pin15 = 3 #blue button int val
	pin16 = 4 #yellow button int val
	input11 = GPIO.input(11) #green button input
	input13 = GPIO.input(13) #red button input
	input15 = GPIO.input(15) #blue button input
	input16 = GPIO.input(16) #yellow button input
	
	chosenButton = 0 #RETURN - Chosen button int value
	sleeptime = 0.03 #Time to sleep between things in seconds

	while (chosenButton==0): #While no button has been pressed, search for button presses
            #If any of the input variables resolve to 1, that means something has been pressed.
            if (input11==1):
                chosenButton = pin11
                time.sleep(sleeptime)
                os.system("espeak -ven+f3 -k5 -s150 'Green button, 1'")
                break
            elif (input13==1):
                chosenButton = pin13
                time.sleep(sleeptime)
                os.system("espeak -ven+f3 -k5 -s150 'Red button, 2'")
                break
            elif (input15==1):
                chosenButton = pin15
                time.sleep(sleeptime)
                os.system("espeak -ven+f3 -k5 -s150 'Blue button, 3'")
                break
            elif (input16==1):
                chosenButton = pin16
                time.sleep(sleeptime)
                os.system("espeak -ven+f3 -k5 -s150 'Yellow button, 4'")
                break
            else:
                pass #If no buttons pressed, do nothing
        time.sleep(0.5)
        os.system("espeak -ven+f3 -k5 -s150 'Returning chosen button.'")
return chosenButton
        
