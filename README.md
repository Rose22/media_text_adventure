# Introduction

MediaTextAdventure is adventure engine with background music, dynamic sounds, and eventually even images that enrich the experience.
It reads from a directory of text files structured in a particular way, and uses that structure as a text adventure experience.

The typewriter makes a sound for every character displayed, which enhances the feel. Coupled with background music, this becomes a multimedia experience instead of just text that you read. There are little sounds for walking to places, quitting the game, etc.

# Requirements
You need python and pygame installed on your system, to use MediaTextAdventure.

# How to create your own adventures
In the adventures/ folder, just create a folder for your adventure.
First off, you will need to create a "start.txt" file. This will be where your player starts the game.
You can optionally also add an "intro.txt" file to add some introduction text to your adventure.

In the text files, you can point to different text files by using this format:  
\[Displayed name for location: location_of_text_file, Another one: location2_text_file\]

In the game, then, you type "go Displayed name for location", and the game will then load "location_of_text_file.txt"

You can use this like:  
\[N: forest, W: town, S: route_2, E: mountain_path]  
For a compass direction-based style :)

To add background music for a particular area, all you need to do is place a music file in the sound/ folder within your adventure folder, with the name of the text file for the location. For example, "mountain_path.mp3"

Some special sounds are:
- typing.wav (typewriter sound)
- gosomewhere.wav (walking sound)
- quit.wav (quitting sound)

You can replace these ones as well.

You can use the standard adventure, Ivania, as a template to create your own :)
