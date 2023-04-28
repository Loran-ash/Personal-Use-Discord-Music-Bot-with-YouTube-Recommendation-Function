import asyncio
import os
import discord
import requests
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv

import utilities
import Recommendation

global url_lst
url_lst=['']

token=open('token.txt','r')
key=token.read()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# TODO: Terminate season after X minutes have passed without interaction.
sessions = []


def check_session(ctx):

    if len(sessions) > 0:
        for i in sessions:
            if i.guild == ctx.guild and i.channel == ctx.author.voice.channel:
                return i
        session = utilities.Session(
            ctx.guild, ctx.author.voice.channel, id=len(sessions))
        sessions.append(session)
        return session
    else:
        session = utilities.Session(ctx.guild, ctx.author.voice.channel, id=0)
        sessions.append(session)
        return session


def prepare_continue_queue(ctx):
    
    fut = asyncio.run_coroutine_threadsafe(continue_queue(ctx), bot.loop)
    try:
        fut.result()
    except Exception as e:
        print(e)


async def continue_queue(ctx):
 
    session = check_session(ctx)
    if not session.q.theres_next():
        await ctx.send("End of the queue.")
        return

    session.q.next()

    voice = discord.utils.get(bot.voice_clients, guild=session.guild)
    source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_OPTIONS)

    if voice.is_playing():
        voice.stop()

    voice.play(source, after=lambda e: prepare_continue_queue(ctx))
    await ctx.send(session.q.current_music.thumb)
    await ctx.send(f"Playing now: {session.q.current_music.title}")


@bot.command(name='play')
async def play(ctx, *, arg=''):
    if arg=='':
        arg=Recommendation.Suggestion(url_lst)

    try:
        voice_channel = ctx.author.voice.channel

    except AttributeError as e:
        print(e)
        await ctx.send("Error")
        return

    session = check_session(ctx)

    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
        try:
            requests.get(arg)
        except Exception as e:
            print(e)
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)[
                'entries'][0]
        else:
            info = ydl.extract_info(arg, download=False)

    url = info['formats'][0]['url']
    thumb = info['thumbnails'][0]['url']
    title = info['title']

    session.q.enqueue(title, url, thumb)

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        await ctx.send(thumb)
        await ctx.send(f"Added to the queue: {title}")
        return
    else:
        await ctx.send(thumb)
        await ctx.send(f"Now playing: {title}")

        url_lst.append(arg)

        session.q.set_last_as_current()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        voice.play(source, after=lambda ee: prepare_continue_queue(ctx))


@bot.command(name='next', aliases=['skip'])
async def skip(ctx):
    session = check_session(ctx)

    if not session.q.theres_next():
        await ctx.send("No song in the queue")
        return

    voice = discord.utils.get(bot.voice_clients, guild=session.guild)

    if voice.is_playing():
        voice.stop()
        return
    else:
        session.q.next()
        source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_OPTIONS)
        voice.play(source, after=lambda e: prepare_continue_queue(ctx))
        return


@bot.command(name='leave')
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected:
        check_session(ctx).q.clear_queue()
        await voice.disconnect()
    else:
        await ctx.send("Bot not connect, so it can't leave.")


@bot.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Error")


@bot.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused:
        voice.resume()
    else:
        await ctx.send("Already paused.")


@bot.command(name='stop')
async def stop(ctx):
    session = check_session(ctx)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing:
        voice.stop()
        session.q.clear_queue()
    else:
        await ctx.send("Error")


bot.run(key)
