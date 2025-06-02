import requests

API_KEY = "8EB492E4D2D1C5722AF0036C4FE09B74"
STEAM_ID = "76561198326195917"
APP_ID = 383180

def get_player_achievements():
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {"key": API_KEY, "steamid": STEAM_ID, "appid": APP_ID}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_game_schema():
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": API_KEY, "appid": APP_ID}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    player_data = get_player_achievements()
    schema_data = get_game_schema()

    if not player_data.get("playerstats") or not player_data["playerstats"].get("achievements"):
        print("Não foi possível obter conquistas do jogador.")
        return

    if not schema_data.get("game") or not schema_data["game"].get("availableGameStats"):
        print("Não foi possível obter esquema do jogo.")
        return

    # Mapeia apiname para título e descrição
    achievements_schema = schema_data["game"]["availableGameStats"].get("achievements", [])
    schema_map = {a["name"]: a for a in achievements_schema}

    missing_achievements = [
        ach for ach in player_data["playerstats"]["achievements"] if ach["achieved"] == 0
    ]

    print(f"Conquistas faltantes ({len(missing_achievements)}):\n")

    for ach in missing_achievements:
        apiname = ach["apiname"]
        title = schema_map.get(apiname, {}).get("displayName", "Sem título")
        desc = schema_map.get(apiname, {}).get("description", "Sem descrição")
        print(f"- {title}\n  {desc}\n")

if __name__ == "__main__":
    main()
