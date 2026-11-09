"""Post a random cat poster to Discord.

A discord.py bot that fetches a random cat image from The Cat API and sends
it as an embed when someone runs the ``!cat`` command. No API key is required
for basic use of The Cat API.

Discord embeds are visible to every bot in the channel by default, so AurInfer
Labs bots see them automatically once invited to the same server and channel.

Run with::

    DISCORD_TOKEN=your_bot_token python3 catposter.py
"""

import json
import logging
import os
import urllib.error
import urllib.request

import discord
from discord.ext import commands

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
REQUEST_TIMEOUT = 10  # seconds

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("catposter")


def fetch_random_cat_poster():
    """Return the URL of a random cat image from The Cat API."""
    try:
        with urllib.request.urlopen(CAT_API_URL, timeout=REQUEST_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise RuntimeError(f"Failed to reach The Cat API: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse The Cat API response: {exc}") from exc

    if not isinstance(data, list) or not data:
        raise RuntimeError("The Cat API returned an empty response.")
    poster_url = data[0].get("url")
    if not poster_url:
        raise RuntimeError("The Cat API response is missing a cat image URL.")
    return poster_url


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Announce that the bot is connected and ready."""
    log.info("Logged in as %s (id: %s)", bot.user, bot.user.id)
    log.info("------")


@bot.event
async def on_command_error(ctx, exc):
    """Handle command errors gracefully."""
    if isinstance(exc, commands.CommandNotFound):
        return
    log.error("Command %s failed: %s", ctx.command, exc)
    await ctx.send("Something went wrong while processing that command.")


@bot.command(name="cat")
async def cat_poster(ctx):
    """Fetch a random cat poster and post it to the channel."""
    try:
        poster_url = fetch_random_cat_poster()
    except Exception as exc:  # noqa: BLE001 - report network failures to the user
        await ctx.send("Could not fetch a cat poster right now. Try again later.")
        log.error("Failed to fetch cat poster: %s", exc)
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
