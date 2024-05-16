"""Module for fetching a PUBG season ID information."""

from dataclasses import dataclass
import requests


@dataclass
class Season:
    """Class representing a PUBG season.

    Fetch a current/specific season id.
    """

    @staticmethod
    def get_current_season_id(header: dict) -> str:
        """Method to fetch current season id.
        
        Params: header
        Returns: 
            str: Current season id.
        """
        url: str = "https://api.pubg.com/shards/steam/seasons"

        r = requests.get(url, headers=header, timeout=10)
        data = r.json()
        current_season_id: dict = []

        for season in data['data']:
            if season['attributes']['isCurrentSeason']:
                current_season_id.append(season)
        
        return current_season_id[0]['id']
    
    @staticmethod
    def get_specific_season_id(number: int, header: dict) -> str:
        """Method to fetch specific season id.
        
        Params: header
        Returns:
            str: Specific season id.
        """
        url: str = "https://api.pubg.com/shards/steam/seasons"

        r = requests.get(url, headers=header, timeout=10)
        if r.status_code != 200:
            return f"Error: Unable to fetch seasons. Status code: {r.status_code}"
        data = r.json()

        for specific_season_id in data['data']:
            if specific_season_id['type'] == 'season' and specific_season_id['id'].startswith('division.bro.official.pc-2018-'):
                extracted_number = int(specific_season_id['id'].split('-')[-1])
                if extracted_number == number:
                    return specific_season_id['id']
        return "Error: Specific season not found."

# EOF
    