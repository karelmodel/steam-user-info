import streamlit as st
from datetime import datetime

dark_style = """
<style>
body, .stApp {
    background-color: #121212;
    color: #e0e0e0;
}
.css-1d391kg { background-color: #1e1e1e; }
.stButton>button { background-color: #3b82f6; color: white; }
a, a:visited { color: #82aaff; }
.message-silver { color: gold; font-weight: bold; font-size: 1.1em; margin-top: 6px; }
.progress-bar-bg {
    background-color: #444; border-radius: 6px; height: 22px; width: 100%;
    margin-top: 4px; margin-bottom: 4px;
}
.progress-bar-fill {
    height: 100%; border-radius: 6px; text-align: center; color: white;
    font-weight: bold; line-height: 22px;
}
.no-achievements-msg {
    margin-top: 4px;
    font-style: italic;
    color: #bbbbbb;
}
.achievement-count {
    font-size: 0.9em;
    color: #ccc;
    margin-bottom: 4px;
}
.card-container {
    display: flex;
    flex-wrap: wrap; /* permite quebra de linha */
    gap: 20px;
    margin-bottom: 30px;
    justify-content: center; /* centraliza horizontalmente */
}
.card {
    padding: 20px;
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 15px rgba(59,130,246,0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: default;
    text-align: center;
    flex: 1 1 200px; /* flex-grow, flex-shrink, flex-basis mínimo */
    max-width: 300px;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(59,130,246,0.8);
}
.card h3 {
    margin: 0 0 8px 0;
}
.card p {
    margin: 0;
    font-size: 1.8em;
    font-weight: bold;
}
/* Cores únicas para cada card */
.card-total-games {
    background: linear-gradient(135deg, #3b82f6, #1e40af);
}
.card-total-achievements {
    background: linear-gradient(135deg, #f59e0b, #b45309);
}
.card-avg-achievements {
    background: linear-gradient(135deg, #10b981, #065f46);
}
.card-total-hours {
    background: linear-gradient(135deg, #ef4444, #7f1d1d);
}
.game-card {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 60px;  /* Espaçamento maior entre os jogos */
    box-shadow: 0 0 8px #111;
    transition: box-shadow 0.3s ease;
    display: flex;
    flex-wrap: wrap; /* Permite quebra interna para colunas */
    gap: 15px;
}
.game-card:hover {
    box-shadow: 0 0 16px #3b82f6;
}
.game-card h2 {
    margin: 0 0 6px 0;
    flex-basis: 100%; /* título ocupa linha toda */
}
.game-card .info {
    color: #bbb;
    font-size: 0.9em;
    margin-bottom: 8px;
    flex-basis: 100%; /* info ocupa linha toda */
}
.game-card .col1, .game-card .col2 {
    flex: 1 1 200px;
    min-width: 150px;
}
.game-card .col1 img {
    width: 100%;
    border-radius: 12px;
    object-fit: cover;
}
</style>
"""

def apply_styles():
    st.markdown(dark_style, unsafe_allow_html=True)

def render_progress_bar(percent: int):
    color = "gold" if percent == 100 else "#3b82f6" if percent > 0 else "#444"
    bar_html = f"""
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="background-color: {color}; width: {percent}%;">{percent}%</div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)

def render_stats_cards(total_games: int, total_achievements: int, avg_percent_achievements: float, total_hours: int):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="card card-total-games">
            <h3>🎮 Jogos</h3>
            <p>{total_games}</p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="card card-total-achievements">
            <h3>🏅 Conquistas</h3>
            <p>{total_achievements}</p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="card card-avg-achievements">
            <h3>🧠 % de Conquistas</h3>
            <p>{avg_percent_achievements:.2f}%</p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="card card-total-hours">
            <h3>⏱️ Tempo de Jogo</h3>
            <p>{total_hours} horas</p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_game_card(game, achievements):
    appid = game['appid']
    header_url = f"https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
    store_url = f"https://store.steampowered.com/app/{appid}/"

    st.markdown(f"""
    <div class="game-card">
        <div class="col1">
            <a href="{store_url}" target="_blank" rel="noopener noreferrer">
                <img src="{header_url}" alt="{game.get('name', 'Jogo')}" />
            </a>
        </div>
        <div class="col2">
            <h2>{game.get('name', 'Sem nome')}</h2>
    """, unsafe_allow_html=True)

    hours = game['playtime_forever'] // 60
    last_played = game.get("rtime_last_played", 0)
    if last_played > 0:
        last_played_str = datetime.utcfromtimestamp(last_played).strftime("%d/%m/%Y")
    else:
        last_played_str = "Nunca"

    st.markdown(f'<div class="info">🕒 {hours} horas jogadas (Último jogo: {last_played_str})</div>', unsafe_allow_html=True)

    achievement_list = achievements.get("achievements", [])
    total = len(achievement_list)
    current = sum(1 for a in achievement_list if a.get("achieved") == 1)
    percent = round((current / total) * 100) if total > 0 else 0

    st.markdown(f'<div class="achievement-count">🏅 {current} de {total} conquistas concluídas</div>', unsafe_allow_html=True)
    render_progress_bar(percent)

    if total == 0:
        st.markdown(f'<div class="no-achievements-msg">❗ Este jogo não possui conquistas.</div>', unsafe_allow_html=True)
    elif percent == 100:
        st.markdown(f'<div class="message-silver">🏆 Todas as conquistas obtidas!</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

def render_filters_sidebar():
    st.sidebar.header("Filtros")
    nome = st.sidebar.text_input("🔍 Buscar por nome")
    conquista_range = st.sidebar.slider(
        "Filtro % Conquistas",
        0, 100, (0, 100),
        help="Selecione o intervalo mínimo e máximo de % de conquistas"
    )
    ordenar_por = st.sidebar.selectbox("Ordenar por", ["Tempo de jogo", "Nome", "% de conquistas"], index=0)
    
    somente_com_conquistas = st.sidebar.checkbox("Mostrar só jogos com conquistas", value=False)

    return {
        "nome": nome,
        "conquista_min": conquista_range[0],
        "conquista_max": conquista_range[1],
        "ordenar_por": ordenar_por,
        "somente_com_conquistas": somente_com_conquistas
    }
