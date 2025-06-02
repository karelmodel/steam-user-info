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

@st.cache_data(show_spinner=False)
def get_game_schema(api_key: str, appid: int):
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": api_key, "appid": appid}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("game", {}).get("availableGameStats", {}).get("achievements", [])
    except requests.RequestException:
        return []

def get_missing_achievements(api_key: str, steam_id: str, appid: int):
    player_data = get_game_achievements(api_key, steam_id, appid)
    schema_data = get_game_schema(api_key, appid)
    schema_map = {a["name"]: a for a in schema_data}
    missing = []

    for ach in player_data.get("achievements", []):
        if ach.get("achieved") == 0:
            apiname = ach.get("apiname", "")
            title = schema_map.get(apiname, {}).get("displayName", "Sem título")
            desc = schema_map.get(apiname, {}).get("description", "Sem descrição")
            missing.append({"title": title, "description": desc})
    return missing
