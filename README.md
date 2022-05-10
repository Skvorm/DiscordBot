# DiscordBot
A simple Discord Bot that allows users to roll various-sided dice(d6,d10,d20,etc) or random numbers in a range, and also allows users to play a very simple card game(assigns card to each user in the calling channel, highest cards win).

## Commands

### -!roll
- Can be used with minimum and maximum range
- Can also be used to emulate dice rolls with a variable number of dice and number of sides      
#### Example
		!roll 1-100 (rolls between 1-100)
		!roll 3d6   (rolls 3 6-sided dice)
		!roll 1d20  (rolls 1 20-sided die)
### -!card
- Draws a card for each user currently in the same voice channel as the sending user. The card with the highest rank is the winner(Very Exciting, I know)
- If not connected to a voice channel, draws a single card for the user and outputs value into the text channel where the command was sent from
        
### -!music
- Allows a user to play audio files in a voice channel
- Server operators can insert media files into "DiscordBot/venv/include/music"
- View playable files with the **!songlist** command and select the corresponding song by including its number after the command. If no/invalid number is    input, random file from folder will play
- ***Requires ffmpeg installation***        
#### Example 
    !music
    !music 5
    !songlist
## Requires
-[Pycord[voice]](https://docs.pycord.dev/en/master/index.html)
	(Base Discord-API libraries for Python)
  
-[Dot-env](https://pypi.org/project/python-dotenv)
	(.env file used to store Discord-API Key)
  
-[FFmpeg](https://ffmpeg.org/)
 (media playback functionality)
	
