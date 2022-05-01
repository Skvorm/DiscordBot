import asyncio
import os
import string
import discord
import contextvars
import datetime as dt
import random
from BotHelperFunctions import BotHelperFunctions
from Game import Game
from dotenv import load_dotenv
from Prediction import Prediction

sv_intents = discord.Intents.default()
sv_intents.members = True
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot_GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client(intents=sv_intents)
b = BotHelperFunctions()
g = Game()


def get_random_song():
    #songs = os.listdir("music")
    songs = b.create_music_list("music")
    song_path = songs[random.randrange(0, len(songs))]
    return song_path
def get_song_choice(user_input):
    #songs = os.listdir("music")
    songs = b.create_music_list("music")
    song_path = songs[user_input-1]
    print(song_path)
    return song_path

def get_song_list_length():
    #return len(os.listdir("music"))
    return len(b.create_music_list("music"))

def song_format(song):
    song_name = song.rsplit("\\")[-1]
    #songtmp = str(song_name.rsplit(".")[0:-1])
    songtmp = song_name[:song_name.rindex(".")]
    #songtmp=songtmp.lstrip("[")
    #songtmp=songtmp.rstrip("]")
    return songtmp
def get_song_list():
    #songs = os.listdir("music")
    songs = b.create_music_list("music")
    ch_ct=0
    ct=1
    out=""
    outtmp=''
    songtmp=''
    bl=2000
    for song in songs:
       #songtmp=song.rstrip("\\.wav\\.m4")
        songtmp =song_format(song)
        outtmp=f'{ct}: {songtmp} \n'
        if len(outtmp)+ch_ct<=bl:
            out+=outtmp
        else:
            #ensures proper output spacing
            #if songlist longer than max Discord message length
            diff=bl-len(out)-1
            out+=diff*' '+"\n"
            out+=outtmp
            ch_ct=0
            print(ch_ct)
        ct+=1
        ch_ct+=len(outtmp)
    return out



@client.event
async def on_ready():
    print(f"{client.user.name} connected")
    print(os.getcwd())
    #print(os.listdir("music"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!songlist"):
    #if message.content.startswith("!songlist"):
        song_list=get_song_list()
        if len(song_list)<1:
            await message.channel.send("no songs to play")
        elif len(song_list)<=2000:
            await message.channel.send(get_song_list())
        else:
            bl=2000
            msg_buffer=[get_song_list()[i:i+bl] for i in range(0,len(song_list),bl)]
            for m in msg_buffer:
                await message.channel.send(m)


    if message.content.startswith("!music"):
       #play_random=False
        print(dt.datetime.now())
        try:
            song_choice=b.parse_song(message.content)
            if song_choice<0 or song_choice>get_song_list_length():
               # play_random=True
                song=get_random_song()
            else:
                song=get_song_choice(song_choice)

            player = message.author.voice.channel
            found = False
            vc_id = 0
            # checks if there is already a voice client playing in one of
            # the discord server's channel and returns that value instead
            # of attempting another connection
            for c in client.voice_clients:
                if c.guild == player.guild:
                    found = True
                    vc_id = c
            if found:
                vc = vc_id
            else:
                vc = await player.connect()

            # disconnects bot from channel after song is finished
            def after_player(error):
                cr = vc.disconnect()
                future = asyncio.run_coroutine_threadsafe(cr, client.loop)
                try:
                    future.result()
                except Exception as e:
                    print(e)
                    #pass

            if vc.is_playing:
                vc.pause()
            #if not play_random:
            #
            #else:
            #   song = get_random_song()

            #vc.play(discord.FFmpegPCMAudio("Cave Theme.wav"), after=after_player)
            try:
                print(song)
                await message.channel.send(f'now playing: "{song_format(song)}"')
                vc.play(discord.FFmpegPCMAudio(song), after=after_player)
                #vc.play(discord.FFmpegPCMAudio("music\\" + song), after=after_player)
            #await message.channel.send(f"playing **{song}**")
            # print(dt.datetime.now())
            except Exception as play_exception:
                print("couldn't play")
                print(str(play_exception))
        except AttributeError:
            print("we've excepted")
            #pass
    if message.content.startswith("!stop"):
        #player = message.author.voice.channel
        player = message.channel
        for p in client.voice_clients:
            if p.guild == player.guild:
                p.stop()
                await p.disconnect()
    if message.content.startswith("!roll"):
        try:
            rng = b.get_roll_range(str(message.content))
        except ValueError:
            # default value of range(1-00), and 1 die
            rng = [1, 100, 1]

        if rng[2] > 1:
            vals = []
            total = 0
            for i in range(0, int(rng[2])):
                roll_val = random.randint(rng[0], rng[1])
                vals.append(roll_val)
                total += roll_val
            roll_val = random.randint(rng[0], rng[1])
            if len(vals) <= 50:
                str_v = str(vals)
                msg = f"**({str(rng[2])}d{str(rng[1])})**: {str(message.author.name)} rolled **{str(total)}**: {str_v}"
            else:
                msg = f"**({str(rng[2])}d{str(rng[1])})**: {str(message.author.name)} rolled **{str(total)}**"
        else:
            roll_val = random.randint(rng[0], rng[1])
            msg = f"**({str(rng[0])}, {str(rng[1])})**: {str(message.author.name)} rolled **{str(roll_val)}**"
        await message.channel.send(msg)
    if message.content == '!card':
        chat_channel = 0
        check = False
        msg = ''
        players = []
        ch_test = message.author.voice
        if ch_test is not None:
            chat_channel = ch_test.channel
            players_m = chat_channel.members
            if len(players_m) >= 1:
                for p in players_m:
                    players.append(p.name)
                    msg = g.play(players, 1)
        else:
            msg = f"**{message.author.name}** : {g.get_random_card()}"
        await message.channel.send(msg)


if __name__ == '__main__':
    time = dt.datetime.now()
    print(f"starting client:{time.strftime('%c')}")
    try:
        client.run(token)
    except Exception as e:
        print("couldn't connect")
