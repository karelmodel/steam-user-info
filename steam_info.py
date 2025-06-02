import streamlit as st
import steam_api
from ui_renderer import render_game_card, render_filters_sidebar, apply_styles, render_stats_cards

st.set_page_config(
    page_title="Meus Jogos na Steam",  # Título da aba do navegador
    page_icon="🎮",  # Ícone da aba (pode ser emoji ou URL)
    layout="wide"
)
apply_styles()

st.title("🎮 Meus Jogos na Steam")

# === BOTÃO PARA LIMPAR CACHE ===
st.sidebar.markdown("## ⚙️ Opções")
if st.sidebar.button("🔄 Recarregar dados"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache limpo! Recarregando...")
    st.rerun()

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "steam_id" not in st.session_state:
    st.session_state.steam_id = ""

query_params = st.query_params

def get_param_value(param):
    val = query_params.get(param, "")
    if isinstance(val, list):
        return val[0] if val else ""
    return val

if st.session_state.api_key == "":
    st.session_state.api_key = get_param_value("api_key")
if st.session_state.steam_id == "":
    st.session_state.steam_id = get_param_value("steam_id")

def update_api_key():
    st.session_state.api_key = st.session_state.api_key_input

def update_steam_id():
    st.session_state.steam_id = st.session_state.steam_id_input

with st.sidebar:
    st.subheader("🔑 Credenciais da Steam")

    api_key_input = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        key="api_key_input",
        type="password",
        on_change=update_api_key
    )
    steam_id_input = st.text_input(
        "Steam ID",
        value=st.session_state.steam_id,
        key="steam_id_input",
        on_change=update_steam_id
    )

    if not st.session_state.api_key or not st.session_state.steam_id:
        st.warning("Por favor, informe sua API Key e Steam ID para continuar.")
        st.stop()

filters = render_filters_sidebar()

progress_bar = st.progress(0)
status_text = st.empty()

owned_games = steam_api.get_owned_games(st.session_state.api_key, st.session_state.steam_id)

filtered_games = []
total = len(owned_games)
total_achievements = 0
total_current_achievements = 0
total_hours = 0

for i, game in enumerate(owned_games):
    status_text.text(f"Carregando dados do jogo {i+1} de {total}...")
    progress_bar.progress(int((i+1) / total * 100))

    if filters["nome"] and filters["nome"].lower() not in game["name"].lower():
        continue

    achievements = steam_api.get_game_achievements(st.session_state.api_key, st.session_state.steam_id, game["appid"])
    total_ach = len(achievements.get("achievements", []))

    if filters.get("somente_com_conquistas", False) and total_ach == 0:
        continue

    current_ach = sum(1 for a in achievements.get("achievements", []) if a.get("achieved") == 1)
    percent = round((current_ach / total_ach) * 100) if total_ach > 0 else 0

    if percent < filters["conquista_min"] or percent > filters["conquista_max"]:
        continue

    game["achievements_data"] = achievements
    game["percent_complete"] = percent
    filtered_games.append(game)

    total_achievements += total_ach
    total_current_achievements += current_ach
    total_hours += game.get("playtime_forever", 0) // 60

progress_bar.empty()
status_text.empty()

if filters["ordenar_por"] == "Tempo de jogo":
    filtered_games.sort(key=lambda x: x.get("playtime_forever", 0), reverse=True)
elif filters["ordenar_por"] == "Nome":
    filtered_games.sort(key=lambda x: x.get("name", ""))
elif filters["ordenar_por"] == "% de conquistas":
    filtered_games.sort(key=lambda x: x.get("percent_complete", 0), reverse=True)

avg_percent_achievements = (total_current_achievements / total_achievements * 100) if total_achievements > 0 else 0

render_stats_cards(
    total_games=len(filtered_games),
    total_achievements=total_achievements,
    avg_percent_achievements=avg_percent_achievements,
    total_hours=total_hours
)

st.markdown("---")

for game in filtered_games:
    achievements_data = game["achievements_data"]
    render_game_card(game, achievements_data)

    missing = steam_api.get_missing_achievements(
        st.session_state.api_key,
        st.session_state.steam_id,
        game["appid"]
    )
    from ui_renderer import render_missing_achievements
    render_missing_achievements(missing, game_name=game['name'])