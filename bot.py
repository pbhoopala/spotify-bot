import discord
import random
import requests
import base64
import json
from discord.ext import commands
from discord import Spotify
from secrets import *

client = commands.Bot(command_prefix = '.')

uris = []

def addSongs(token, playlist_id):
    endPoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    data_body = json.dumps(uris)
    res = requests.post(url=endPoint, data=data_body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})

def createPlaylist(token, name, desc, public):
    endPoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data_body = json.dumps({
        "name": name,
        "description": desc,
        "public": public
    })
    res = requests.post(url=endPoint, data=data_body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})

#API requests
playlist_id = " "

@client.event
async def on_ready():
    print('Bot is live.')

@client.command()
async def hello(ctx, member : discord.Member = None):
    member = member or ctx.author
    await ctx.send(f'Hello {member.display_name}!')

@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

@client.command()
async def spotifyEmbed(ctx, title1, artist1, album, song, trackid):
    embed = discord.Embed(title="Adding " + title1 + " to the playlist!", description=title1 + " by " + artist1, color=discord.Color.green())
    embed.set_footer(text="Sent by " + ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url=album)
    embed.add_field(name="Song link:", value="[" + song + "](https://open.spotify.com/track/" + trackid + ")")

    await ctx.send(embed=embed)

@client.command()
async def add(ctx, member : discord.Member = None):
    member = member or ctx.author
    for activity in member.activities:
        if type(member.activity) == discord.Spotify:
            trackid = activity.track_id
            album = activity.album_cover_url
            uri = "spotify:track:"+trackid
            title = activity.title
            artist = activity.artist
            song = activity.title
            uris.append(uri)
            await spotifyEmbed(ctx, title, artist, album, song, trackid)
            addSongs(OAtoken, playlist_id)
            uris.remove(uri)

@client.command(aliases=["create", "playlist"])
async def createplaylist(ctx, member : discord.Member = None):
    member = member or ctx.author
    for activity in member.activities:
        if type(member.activity) == discord.Spotify:
            await ctx.send("Please enter playlist name:")
            nameTest = await client.wait_for('message')
            name = nameTest.content
            await ctx.send("Please enter a description:")
            descTest = await client.wait_for('message')
            desc = descTest.content
            createPlaylist(OAtoken, name, desc, True)
            await ctx.send("Your playlist has been created under the account name pbhoopala!")


client.run(discordToken)
