import requests
import os
from dotenv import load_dotenv
import storage.db as db

load_dotenv()

API_KEY = os.getenv('RIOT_API_KEY')
headers = {
    "X-RIOT-TOKEN": API_KEY
}

def fetch_puuid(gameName: str, tagLine: str) -> str:
    response = requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}', headers=headers)
    account = response.json()
    return account["puuid"]

def fetch_match_ids(puuid: str, count: int = 20) -> list[str]:
    if count < 0 or count > 100:
        raise ValueError("Count must be between 0 and 100")
    
    response = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}', headers=headers)
    return response.json()

def fetch_match(matchId: str) -> dict:
    response = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}', headers=headers)
    return response.json()
    
def fetch_match_timeline(matchId: str) -> dict:
    response = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline', headers=headers)
    return response.json()