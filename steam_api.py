import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def get_owned_games(api_key: str, steam_id: str):
    url = (
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        f"?key={api_key}&steamid={steam_id}&include_appinfo=1&format=json"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    games = data.get("response", {}).get("games", [])
    return games

@st.cache_data(show_spinner=False)
def get_game_achievements(api_key: str, steam_id: str, appid: int):
    url = (
        f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
        f"?key={api_key}&steamid={steam_id}&appid={appid}&format=json"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        achievements = data.get("playerstats", {}).get("achievements", [])
        return {"achievements": achievements}
    except requests.HTTPError:
        return {"achievements": []}
