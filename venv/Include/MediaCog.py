import asyncio
import discord
from discord.ext import commands
from BotHelperFunctions import get_song_list, parse_song, get_song_list_length, get_random_song, get_song_choice, \
    song_format


class Media(commands.Cog, name="Media"):
    def __init__(self, client):
        self.client = client

    command_song_list_desc = "Lists playable media files"
    command_song_list_help_long = "Song Numbers for !music command"
    command_song_list_help_brief = "Song Numbers for !music command"

    @discord.slash_command(
        name="songlist",
        description=command_song_list_desc,
        help=command_song_list_help_long,
        brief=command_song_list_help_brief)
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

    song_desc = "Plays media files"
    song_help_long = "View playable files with the !songlist command and select the corresponding song \
                    by including its number after the command. If no/invalid number is input, random \
                    file from folder will play"

    @discord.slash_command(
        description=song_desc,
        name="music",
        help=song_help_long,
        brief=song_desc)
    async def music(self, ctx, song_number: discord.Option(str, "Enter Song Number", required=False, default='')):
        ran = False
        try:
            song_choice = parse_song(song_number)
            if song_choice < 0 or song_choice > get_song_list_length():
                rand_song = get_random_song()
                song = rand_song[1]
                song_choice = rand_song[0]
                ran = True
            else:
                song = get_song_choice(song_choice)
            # print(str(ran))
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
                except Exception as e2:
                    print(e2)

            if vc.is_playing:
                vc.pause()
            try:
                # print(song)
                vc.play(discord.FFmpegPCMAudio(song), after=after_player)
                # await ctx.send(f'Now playing: "{song_format(song)}"')
                if ran:
                    t = "Random Play"
                else:
                    t = "Request"
                emb = discord.Embed(
                    # title="Media",
                    description=f'Now playing: **{song_format(song)}**',
                    color=discord.Color.dark_blue())
                # emb.add_field(name="Now Playing",value=f"{song_format(song)}")
                emb.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                emb.set_footer(text=t + f': Song #{song_choice}')

                await ctx.respond(embed=emb)

            except Exception as play_exception:
                print("couldn't play")
                print(str(play_exception))
        except AttributeError as e:
            # print("we've excepted"+str(e))
            pass

    stop_desc = "Stops the music"
    stop_help = "Stops the currently playing music"
    stop_help_brief = "Stops the currently playing music"

    @discord.slash_command(
        name="stop",
        desc=stop_desc,
        help=stop_help,
        brief=stop_help_brief)
    async def stop(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.stop()
                await p.disconnect()

    pause_desc = "Pauses the music"
    pause_help = "Pauses the currently playing music"
    pause_help_brief = "Pauses the currently playing music"

    @discord.slash_command(
        name="pause",
        desc=pause_desc,
        help=pause_help,
        brief=pause_help_brief)
    async def pause(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.pause()

    resume_desc = "Resumes playing paused music"
    resume_help = "Resumes playing the music"
    resume_help_brief = "Resumes paused music"

    @discord.slash_command(
        name="resume",
        desc=resume_desc,
        help=resume_help,
        brief=resume_help_brief)
    async def resume(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.resume()


def setup(client):
    client.add_cog(Media(client))
