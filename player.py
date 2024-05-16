"""Module for fetching a PUBG player's stats and account ID."""

from dataclasses import dataclass
import requests


@dataclass
class Player:
    """Class representing a PUBG player's profile.
    
    Fetch a player stats for a specified season and game mode.
    """
    player_name: str
    platform: str

    def get_player_season_stats(self, player_id, season_id: str, header: dict, mode: str) -> str:
        """Fetch a specified player's stats for a given game mode.
        
        Params: player_id, season_id, header, mode (e.g., 'solo-fpp', 'duo-fpp', 'squad-fpp')
        Returns: 
            str: Player stats for the season and mode.
        """
        url: str = f"https://api.pubg.com/shards/{self.platform}/players/{player_id}/seasons/{season_id}"

        r = requests.get(url, headers=header, timeout=10)
        if r.status_code != 200:
            return f"Error: Unable to fetch data for {self.player_name}. Status code: {r.status_code}"
        data = r.json()
        try:
            stats = data['data']['attributes']['gameModeStats'][mode]
        except KeyError:
            return f"Error: No stats available for {self.player_name} in mode {mode}."

        formatted_stats: str = f"\n{mode.capitalize()}:\n"
        for key, value in stats.items():
            formatted_stats += f"{key.capitalize()}: {value}\n"

        return formatted_stats

    def get_player_id(self, header: dict) -> str:
        """Parse JSON data to fetch a player's account ID from a specified username.

        Params: header
        Returns:
            str: Player account ID.
        """
        url: str = f"https://api.pubg.com/shards/{self.platform}/players?filter[playerNames]={self.player_name}"

        r = requests.get(url, headers=header, timeout=10)
        if r.status_code != 200:
            return f"Error: Unable to fetch player ID for {self.player_name}. Status code: {r.status_code}"
        json_data = r.json()
        try:
            data = json_data['data'][0]
            player_id = data['id']
        except (IndexError, KeyError):
            return "Error: Player not found."

        return player_id
        
# EOF
