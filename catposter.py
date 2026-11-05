"""Post a random cat poster to Discord.

A discord.py bot that fetches a random cat image from The Cat API and sends
it as an embed when someone runs the ``!cat`` command. No API key is required
for basic use of The Cat API.

Run with::

    DISCORD_TOKEN=your_bot_token python3 catposter.py
"""

import json
import os
import urllib.request

import discord
from discord.ext import commands

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


def fetch_random_cat_poster():
    """Return the URL of a random cat image from The Cat API."""
    with urllib.request.urlopen(CAT_API_URL) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data[0]["url"]


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Announce that the bot is connected and ready."""
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    print("------")


@bot.command(name="cat")
async def cat_poster(ctx):
    """Fetch a random cat poster and post it to the channel."""
    try:
        poster_url = fetch_random_cat_poster()
    except Exception as exc:  # noqa: BLE001 - report network failures to the user
        await ctx.send("Could not fetch a cat poster right now. Try again later.")
        print(f"Failed to fetch cat poster: {exc}")
        return

    embed = discord.Embed(title="Random Cat Poster", colour=discord.Colour.orange())
    embed.set_image(url=poster_url)
    await ctx.send(embed=embed)


def main():
    """Connect the bot to Discord using the DISCORD_TOKEN environment variable."""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("Set the DISCORD_TOKEN environment variable before running.")
    bot.run(token)


if __name__ == "__main__":
    main()
