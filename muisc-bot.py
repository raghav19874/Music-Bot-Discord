import discord
from discord.ext import commands, tasks
import youtube_dl
import os
from random import choice
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')
@client.event
async def on_ready():
    print('Bot is online!')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `!help` command for details!')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Music-Bot commands",
        description="All commands listed below",
        color=discord.Color.red(),
        author="Raghav"
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1071582837030060032/kKV-I01n.jpg")
    embed.add_field(name="!help", value="Gives a list of all commands", inline="False")
    embed.add_field(name="!ping", value="This command returns the latency", inline="False")
    embed.add_field(name="!hello", value="This command returns a welcome message", inline="False")
    embed.add_field(name="!die", value="This command returns last words", inline="False")
    embed.add_field(name="!credits", value="This command returns the TRUE credits", inline="False")
    embed.add_field(name="!join", value="This command makes the bot join the voice channel", inline="False")
    embed.add_field(name="!disconnect", value="This command makes the bot disconnect from the voice channel", inline="False")
    embed.add_field(name="!play", value="This command plays the music", inline="False")
    embed.add_field(name="!pause", value="This command pauses the music", inline="False")
    embed.add_field(name="!resume", value="This command resumes the music", inline="False")
    embed.add_field(name="!stop", value="This command stops the music", inline="False")

    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'**WTF!!** Latency: {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi','Well, I am not interested!!', '**Wasssuup!**']
    await ctx.send(choice(responses))

@client.command()
async def die(ctx):
    responses = ['Why have you brought my short life to an end?', 'I could have done so much more...', 'I have a family, kill them instead', f'**Well!!** You Die..!!']
    await ctx.send(choice(responses))

@client.command()
async def credits(ctx):
    await ctx.send('**No one but me, loser!**')

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@join.error
async def join_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You must join the voice channel first!!")

@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()
    await client.change_presence(activity=None)
@disconnect.error
async def disconnect_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("The Bot must be connected to a voice channel to use this command")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await("Wait for the current song to end or use the stop command first")
        return

    voice = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

    activity = discord.Activity(
        name="music",
        type=discord.ActivityType.playing
    )
    await client.change_presence(activity=activity)


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You must join the voice channel first")

@client.command()
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nothing is playing right now")
@pause.error
async def pause_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You must join the voice channel first")

@client.command()
async def resume(ctx):
    voice = ctx.voice_client
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The song is not paused")
@resume.error
async def resume_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You must join the voice channel first")

@client.command()
async def stop(ctx):
    voice = ctx.voice_client
    voice.stop()
@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You must join the voice channel first")

client.run("TOKEN")
