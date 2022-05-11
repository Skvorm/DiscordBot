import asyncio
import discord
from discord.ext import commands
from BotHelperFunctions import get_song_list, parse_song, get_song_list_length, get_random_song, get_song_choice, \
    song_format


class Media(commands.Cog, name="Media"):
    def __init__(self, client):
        self.client = client

    songlist_desc = "Lists playable media files"
    songlist_help_long = "Song Numbers for !music command"
    songlist_help_brief = "Song Numbers for !music command"

    @commands.command(name="songlist", aliases=["musiclist", "list"], description=songlist_desc,
                      help=songlist_help_long, brief=songlist_help_brief)
    async def song_list(self, ctx):
        bl = 2000
        song_list = get_song_list()
        if len(song_list) < 1:
            await ctx.channel.send("No media files in \\music folder")
        elif len(song_list) <= bl:
            await ctx.channel.send(song_list)
        else:
            msg_buffer = [song_list[i:i + bl] for i in range(0, len(song_list), bl)]
            for m in msg_buffer:
                await ctx.send(m)

    song_desc="plays media files"
    song_help_long="View playable files with the !songlist command and select the corresponding song \
                    by including its number after the command. If no/invalid number is input, random \
                    file from folder will play"
    song_help_brief='plays media files'

    @commands.command(name="music", aliases=["song", "play", "media"],description=song_desc,help=song_help_long,
                      brief=song_help_brief,rest_is_raw=True)
    async def music(self, ctx, *, arg):
        try:
            song_choice = parse_song(arg)
            if song_choice < 0 or song_choice > get_song_list_length():
                song = get_random_song()
            else:
                song = get_song_choice(song_choice)

            player = ctx.author.voice.channel
            found = False
            vc_id = 0
            # checks if there is already a voice client playing in one of
            # the discord server's channel and returns that value instead
            # of attempting another connection
            for c in self.client.voice_clients:
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
                future = asyncio.run_coroutine_threadsafe(cr, self.client.loop)
                try:
                    future.result()
                except Exception as e:
                    print(e)

            if vc.is_playing:
                vc.pause()
            try:
                # print(song)
                vc.play(discord.FFmpegPCMAudio(song), after=after_player)
                await ctx.send(f'Now playing: "{song_format(song)}"')

            except Exception as play_exception:
                print("couldn't play")
                print(str(play_exception))
        except AttributeError as e:
            # print("we've excepted"+str(e))
            pass

    stop_desc="stops the music"
    stop_help="stops the currently playing music"
    stop_help_brief="stops the currently playing music"

    @commands.command(name="stop",desc=stop_desc,help=stop_help,brief=stop_help_brief)
    async def stop(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.stop()
                await p.disconnect()


def setup(client):
    client.add_cog(Media(client))
