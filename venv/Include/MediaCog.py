import asyncio
import discord
from discord.ext import commands, bridge
from BotHelperFunctions import get_song_list, parse_song, get_song_list_length, get_random_song, get_song_choice, \
    song_format


class Media(commands.Cog, name="Media"):
    def __init__(self, client):
        self.client = client

    media="Media"
    command_song_list_desc = "Lists playable media files"
    command_song_list_help_long = "Song Numbers for !music command"
    command_song_list_help_brief = "Song Numbers for !music command"

    @bridge.bridge_command(
        name="songlist",
        description=command_song_list_desc,
        cog="Media",
        group=media,
        help=command_song_list_help_long,
        brief=command_song_list_help_brief)
    async def song_list(self, ctx):
        bl = 2000
        song_list = get_song_list()
        if len(song_list) < 1:
            await ctx.channel.send("No media files in \\music folder")
        elif len(song_list) <= bl:
            await ctx.channel.respond(song_list)
        else:
            msg_buffer = [song_list[i:i + bl] for i in range(0, len(song_list), bl)]
            await ctx.respond("Generating Songlist")
            for m in msg_buffer:
                await ctx.send(m)

    song_desc = "Plays media files"
    song_help_long = "View playable files with the !songlist command and select the corresponding song \
                    by including its number after the command. If no/invalid number is input, random \
                    file from folder will play"

    @bridge.bridge_command(
        description=song_desc,
        cog="Media",
        group=media,
        aliases=["song", "play", "media"],
        help=song_help_long,
        brief=song_desc,
        rest_is_raw=True)
    async def music(self, ctx, * , song_number=""):
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

                if type(ctx) is discord.commands.context.ApplicationContext:
                    await ctx.respond(embed=emb)
                else:
                    await ctx.respond(embed=emb)

            except Exception as play_exception:
               # print("couldn't play")
                print(str(play_exception))
               # print("1")
        except AttributeError as e:
            # print("we've excepted"+str(e))
            if type(ctx) is discord.commands.context.ApplicationContext:
                await ctx.respond("couldn't play music",ephemeral=True)

    stop_desc = "Stops the music"
    stop_help = "Stops the currently playing music"
    stop_help_brief = "Stops the currently playing music"

    @bridge.bridge_command(
        name="stop",
        desc=stop_desc,
        cog="Media",
        group=media,
        help=stop_help,
        brief=stop_help_brief)
    async def stop(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.stop()
                await p.disconnect()
                await ctx.respond("Playback stopped")

    pause_desc = "Pauses the music"
    pause_help = "Pauses the currently playing music"
    pause_help_brief = "Pauses the currently playing music"

    @bridge.bridge_command(
        name="pause",
        desc=pause_desc,
        cog="Media",
        group=media,
        help=pause_help,
        brief=pause_help_brief)
    async def pause(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.pause()
                await ctx.respond("Media Playback is paused.")

    resume_desc = "Resumes playing paused music"
    resume_help = "Resumes playing the music"
    resume_help_brief = "Resumes paused music"

    @bridge.bridge_command(
        name="resume",
        desc=resume_desc,
        cog="Media",
        group=media,
        help=resume_help,
        brief=resume_help_brief)
    async def resume(self, ctx):
        player = ctx.channel
        for p in self.client.voice_clients:
            if p.guild == player.guild:
                p.resume()
                await ctx.respond("Resuming media playback")


def setup(client):
    client.add_cog(Media(client))
