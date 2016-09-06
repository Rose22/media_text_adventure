#!/usr/bin/env python

import sys, time, os, pygame

#########
# A text adventure engine unlike any other.. with background music, dynamic sounds, and eventually even images that enrich the experience.
# It reads from a directory of text files structured in a particular way, and uses that structure as a text adventure experience.
#
# For example: the directory must contain a file named "start". This is the point where you start out.
# The top of it will read [N: road, E: nothing, S: nothing, W: nothing]
# This means that from the start point, the player can travel North, to the road.
# If he does travel to the North, the text adventure engine will read the file "road.txt" and use that to play out the next stage of the adventure.
# The typewriter already makes a sound for every character displayed, which already enhances the feel. Coupled with background music, this becomes a multimedia experience instead of just text that you read.
# Creators can assign custom sounds to every action, by replacing the standard sounds in "sound/" with their own.
# To add background music for a particular area, all the creator needs to do is place a music file in sound/ with the name of the location. For example, "road.mp3"

#########
# Copyright (c) 2016 Rose (Rose22)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

######
# Function definitions
def game_menu():
	print "MediaTextAdventure 1.0 by Rose22"
	print "Choose an adventure: "
	print
	
	cwd_contents = os.listdir('.')
	i = 0
	adventures = []
	for file in cwd_contents:
		if os.path.isdir(file):
			print "%i) %s" % (i, file)
			adventures.append(file)
			i += 1
			
	while True:
		chosen_adventure = raw_input("Which one?> ")
		if chosen_adventure in ("exit", "quit"):
			sys.exit(0)
		try:
			chosen_adventure = int(chosen_adventure)
		except:
			print "Invalid choice."
			continue
		
		if len(adventures) > chosen_adventure:
			return adventures[chosen_adventure]
		else:
			print "Invalid choice."
			pass
			
def quitgame():
	global playing_adventure
	
	if pygame.mixer.music.get_busy:
		pygame.mixer.music.fadeout(1000)
	if quitSound: quitSound.play()
	time.sleep(0.3)
	
	playing_adventure = False

def restartgame():
	global location
	global nodirections
	
	# Restart the game
	if pygame.mixer.music.get_busy:
		pygame.mixer.music.fadeout(1000)
	location = "start"
	nodirections = False
	
	clearscreen()
	display_intro()
	pygame.mixer.music.set_volume(100)

def clearscreen():
	os.system('cls' if os.name=='nt' else 'clear')

def typewriter (text):
	for character in text:
		if typingSound: typingSound.play()
		sys.stdout.flush()
		sys.stdout.write(character)
		time.sleep(0.03)

		if character == "\n":
			time.sleep(0.5)
			
def display_intro():
	if os.path.isfile(adventureDir + os.sep + "intro.txt"):
		introFile = open(adventureDir + os.sep + "intro.txt", "r")
		introContents = introFile.read()
		introFile.close()

		typewriter(introContents)
		print
		print
			
def gameover ():
	print
	pygame.mixer.music.fadeout(300)
	if gameoverSound: gameoverSound.play()
	typewriter("GAME OVER\n")
	print "Try again? (Y/N)>",
	answer = raw_input()
	
	if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
		restartgame()
	else:
		typewriter("You leave the world of " + adventureDir.rstrip('/') + ".\n")
		quitgame()

######
# Initialization
os.chdir("adventures")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

running = True
try:
	while running:
		adventureDir = game_menu()
		
		folderContents = os.listdir(adventureDir)
		soundDir = adventureDir + "/sounds/"

		if os.path.isfile(soundDir + 'typing.wav'):
			typingSound = pygame.mixer.Sound(soundDir + 'typing.wav')
			typingSound.set_volume(0.2)
		else:
			typingSound = False

		if os.path.isfile(soundDir + 'gameover.wav'):
			gameoverSound = pygame.mixer.Sound(soundDir + 'gameover.wav')
			gameoverSound.set_volume(0.5)
		else:
			gameoverSound = False

		if os.path.isfile(soundDir + 'gosomewhere.wav'):
			goSound = pygame.mixer.Sound(soundDir + 'gosomewhere.wav')
			goSound.set_volume(1)
		else:
			goSound = False

		if os.path.isfile(soundDir + 'quit.wav'):
			quitSound = pygame.mixer.Sound(soundDir + 'quit.wav')
			quitSound.set_volume(1)
		else:
			quitSound = False

		location = "start"

		nodirections = False
		loadedMusic = ""

		clearscreen()
		display_intro()
		
		playing_adventure = True
		while playing_adventure:
			try:
				adventureFile = open(adventureDir + os.sep + location + ".txt", "r")

				# The first line contains the directions the player can go to
				# This entire part creates a dictionary that contains the location the player can go to for every direction (N, E, S, W)
				directionData = adventureFile.readline().rstrip()
				directionData = directionData.replace('[', '').replace(']','')

				directionsRaw = directionData.split(", ")
				directions = {}
				try:
					for direction in directionsRaw:
						directionSplit = direction.split(': ')

						directions[directionSplit[0]] = directionSplit[1]
				except:
					nodirections = True;

				# Skip the second line of the file, as it is usually (and should be) an empty line.
				adventureFile.readline()

				adventureBuffer = adventureFile.read()
				adventureFile.close()

				# Load and play the music for the location. Make sure that it doesn't load the same music again if it is already playing.
				newMusic = soundDir + location
				if os.path.isfile(newMusic + '.wav') and loadedMusic != newMusic + '.wav':
					pygame.mixer.music.load(soundDir + location + '.wav')
					time.sleep(0.1)
					pygame.mixer.music.play(-1)
					loadedMusic = soundDir + location + '.wav'
				if os.path.isfile(soundDir + location + '.mp3') and loadedMusic != newMusic + '.mp3':
					pygame.mixer.music.load(soundDir + location + '.mp3')
					time.sleep(0.1)
					pygame.mixer.music.play(-1)
					loadedMusic = soundDir + location + '.mp3'

				# Write out the adventure text
				typewriter(adventureBuffer)
				print

				if location == 'suicide':
					gameover()

				print
				print "You can go:"
				if nodirections == False:
					for printeddirection, printedlocation in sorted(directions.iteritems()):
						if printedlocation == 'start':
							printedlocation = 'the beginning'
						print printeddirection.title() + ", to " + printedlocation.replace('_', " ").title()
					nodirections = False
				else:
					print "Nowhere"
			except IOError:
				print "The engine tried to load a file/location that does not exist. Tell the creator of the game that one of the locations is missing from the game. Location name: " + location
			except:
				sys.exit()
		
			askingForInput = True
			while ( askingForInput ):
				print
				print "What do you do?>",
				playerAction = raw_input()
				playerActionSplit = playerAction.split(' ')
				playerCommand = playerActionSplit[0].lower()
				playerCommandArguments = ' '.join(playerActionSplit[1:])

				travelled = False
				if playerCommand == 'go':
					for nextDirection, nextLocation in directions.iteritems():
						if playerCommandArguments.lower() == nextDirection.lower() and nextLocation != 'nothing':
							location = nextLocation
							travelled = True
					if travelled:
						if goSound: goSound.play()
						time.sleep(1)
						clearscreen()
						askingForInput = False
					else:
						typewriter("You can't go there.")
					travelled = False
				elif playerCommand == 'look':
					askingForInput = False
				elif playerCommand == 'nothing':
					typewriter("You do nothing. Nothing happens as a result.")
				elif playerCommand == 'say':
					if playerCommandArguments == '':
						playerCommandArguments = "I don't know what to say!"
					typewriter("You say: " + playerCommandArguments)
				elif playerCommand == 'eat':
					typewriter("You eat " + playerCommandArguments + '.')
				elif playerCommand == 'suicide':
					location = 'suicide'
					askingForInput = False
				elif playerCommand == 'slap':
					if playerCommandArguments != '':
						typewriter("You slap " + playerCommandArguments + ". He/she gives you a menacing glare in return.")
					else:
						typewriter("You slap yourself. It hurts.")
				elif playerCommand == 'quit' or playerCommand == 'exit':
					typewriter("You leave the world of " + adventureDir.rstrip('/') + ".\n")
					time.sleep(0.5)
					clearscreen()
					quitgame()
					askingForInput = False
				elif playerCommand == 'restart' or playerCommand == "replay":
					restartgame()
					askingForInput = False
				else:
					typewriter("Sorry, no can do.")
except:
	print
