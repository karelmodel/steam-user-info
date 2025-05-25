# Steam User Info App

Um app feito com Streamlit que exibe seus jogos da Steam, conquistas e estatísticas, com filtros e interface visual amigável. Você pode inserir sua API Key e Steam ID manualmente ou via parâmetros na URL.

## 🚀 Demonstração

Você pode abrir a aplicação localmente com:

    streamlit run steam_info.py

Ou acessar diretamente com:

    http://localhost:8501/?api_key=SUA_API_KEY&steam_id=SEU_STEAM_ID

## 🔧 Como usar

1. Clone o repositório:

   ```
    git clone https://github.com/karelmodel/steam-user-info.git
    cd steam-user-info
   ```

2. Instale as dependências:

   ```
   pip install -r requirements.txt 
   ```

3. Execute o app:

   ```
    streamlit run steam_info.py
   ```

4. Insira sua API Key e Steam ID na sidebar ou via URL:

   ```
    http://localhost:8501/?api_key=8EB492E4D2D1C5722AF0036C4FE09B74&steam_id=76561198326195917
   ```

## 📦 Requisitos

- Python 3.8 ou superior
- Conta Steam com perfil público
- API Key da Steam: https://steamcommunity.com/dev/apikey

## 📁 Estrutura

    steam-user-info/
    ├── steam_info.py         # App principal do Streamlit
    ├── steam_api.py          # Funções para chamadas à API da Steam
    ├── ui_renderer.py        # Componentes visuais da interface
    ├── requirements.txt      # Dependências do projeto
    ├── .gitignore            # Arquivos ignorados pelo Git
    └── README.md             # Este arquivo

## 🧠 Funcionalidades

- Filtro por nome do jogo
- Filtro por jogos com conquistas
- Filtro por % de conquistas
- Ordenação por tempo de jogo, nome ou % de conquistas
- Barra de progresso de conquistas por jogo
- Cards de estatísticas gerais

## 🔐 Segurança

A API Key informada não é armazenada em arquivos, apenas na sessão do navegador ou como parâmetro da URL.

## 📃 Licença

MIT
