# Personal-Use-Discord-Music-Bot-with-YouTube-Recommendation-Function

Personal use discord music bot with YouTube recommendation function using Python

The code of music bot is based on Gabriel-M-Martins/Discord-MusicBot.

Recommendation System.ipynb mainly deals with raw datasets. Because the .csv files are too large, I didn't upload them here. The analyzed data is already saved to result.csv.

Set up:

1.You can visit the website of the original code for guide of installation: https://github.com/Gabriel-M-Martins/Discord-MusicBot. This bot has dependencies on FFmpeg, youtube_dl, dotenv, PyNaCl and (obviously) discord.py. Make sure all of the requirements are satisfied.

2.You only need four of these files. Recommendation System.ipynb is unnecessary.

3.After downloading those files, You need to create a file named token.txt under the same folder that contains only your Discord Bot token.(You can check it on the Discord Developer Portal website, copy and paste.)

4.Run main.py

Commands:

/play : Searchs for the author's current voice channel, joins it and plays the requested song, which can be a url to a video on YouTube or a simple search.
/play : Without url after the command. This will recommand you a new song according to your previously played songs.
/skip : Goes to next song.
/pause : Pauses the current song.
/resume : Resumes the current song.
/stop : Stops playing the current song and clears the queue.
/leave : Leaves the voice channel.
/print : Only for debugging, returns the session ID, what is currently playing and what is on the queue.

