"""Runs a discord bot that fetches and displays PUBG player statistics."""

import os
from typing import Final, Dict
from dotenv import load_dotenv
import discord
from discord.ext import commands
from player import Player
from season import Season


def main():
    """Run the Discord bot."""
    load_dotenv()
    token: Final[str] = os.getenv('DISCORD_TOKEN')
    api_key: str = os.getenv('PUBG_API_KEY')

    intents = discord.Intents.default()
    intents.message_content = True  
    bot = commands.Bot(command_prefix='$', intents=intents)

    header: Dict[str, str] = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    @bot.event
    async def on_guild_join(guild):
        general_channel = None
        for channel in guild.text_channels:
            if "general" in channel.name:
                general_channel = channel
                break
        if general_channel is None:
            general_channel = guild.text_channels[0]

        await general_channel.send("Wazzzzzzzzup! I'm a PUBG stats bot. Use the command `$stats <season number> <PUBG username> < gamemode>` to get started!\nEx: $stats 29 Wonkamaster101 fpp-squad\nAvailable Seasons: 1-29\nAvailable Gamemodes: fpp-solo, fpp-duo, fpp-squad")

    @bot.command(name='stats')
    async def stats(ctx, specific_season_id: int, player_name: str, game_mode: str):
        player = Player(player_name=player_name, platform="steam")
        player_id = player.get_player_id(header)

        if 'Error' in player_id:
            await ctx.send(player_id)
            return

        season_id = Season.get_specific_season_id(specific_season_id, header)
        if 'Error' in season_id:
            await ctx.send(season_id)
            return

        game_mode = game_mode.lower()
        if game_mode not in ['fpp-solo', 'fpp-duo', 'fpp-squad']:
            await ctx.send("Invalid game mode. Use 'fpp-solo', 'fpp-duo', or 'fpp-squad'.")
            return

        game_mode_stats = {
            'fpp-solo': 'solo-fpp',
            'fpp-duo': 'duo-fpp',
            'fpp-squad': 'squad-fpp'
        }

        stats = player.get_player_season_stats(player_id, season_id, header, game_mode_stats[game_mode])
        await ctx.send(f"Fetching {game_mode} stats for {player_name}\n")
        await ctx.send(stats)

    bot.run(token)

if __name__ == "__main__":
    main()

# EOF
