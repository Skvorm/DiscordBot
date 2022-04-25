# DiscordBot
A simple Discord Bot that allows users to roll various-sided dice(d6,d10,d20,etc) or random numbers in a range, and also allows users to play a very simple card game(assigns card to each user in the calling channel, highest cards win).

## Commands

### -!roll
- Can be used with minimum and maximum range
- Can also be used to emulate dice rolls with a variable number of dice and number of sides      
#### Example
		!roll 1-100
		!roll 3d6
		!roll 1d20 
### -!card
- draws a card for each user currently in the same voice channel as the sending user. The card with the highest rank is the winner.(Very Exciting, I know)
- if not connected to a voice channel, draws a single card for the user and outputs value into the text channel where the command was sent.
        
### -!music
- allows a user to play audio files in a voice channel
- Server operators can insert media files into "DiscordBot/venv/include/music"
- view playable files with the **!songlist** command and select the corresponding song by including its number after the command. If no/invalid number is    input, random file from folder will play.
- ***Requires ffmpeg installation***        
#### Example 
    !music
    !music 5
    !songlist
## Requires
-[Discord.py[voice]](https://discordpy.readthedocs.io/en/latest)
	(Base Discord-API libraries for Python)
  
-[Dot-env](https://pypi.org/project/python-dotenv)
	(.env file used to store Discord-API Key)
  
-[FFmpeg](https://ffmpeg.org/)
 (media playback functionality)
	
