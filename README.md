# Steam Info - Meus Jogos na Steam

Aplicação web em Streamlit que conecta à API da Steam para mostrar seus jogos, conquistas, tempo de jogo e filtros personalizados.

---

## Funcionalidades

- Listagem dos jogos possuídos na Steam com nome, horas jogadas e conquistas.
- Filtragem por nome do jogo, percentual de conquistas e jogos com conquistas.
- Ordenação por nome, tempo de jogo e percentual de conquistas.
- Entrada das credenciais (API Key e Steam ID) via interface ou URL (parâmetros GET).
- Visualização de progresso e estatísticas gerais.
- Layout responsivo e fácil de usar.

---

## Requisitos

- Python 3.8+
- Streamlit
- Requests

---

## Instalação

1. Clone o repositório:

   git clone https://github.com/karelmodel/steam-user-info.git
   cd steam-user-info

2. Crie um ambiente virtual (opcional, mas recomendado):

   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows

3. Instale as dependências:

   pip install -r requirements.txt

---

## Como usar

1. Execute o app localmente:

   streamlit run steam_info.py

2. Informe sua API Key e Steam ID na barra lateral ou passe via URL:

   http://localhost:8501/?api_key=SUA_API_KEY&steam_id=SEU_STEAM_ID

3. Aproveite a visualização dos seus jogos e conquistas!

---

## Deploy

Recomendamos usar o Streamlit Cloud (https://share.streamlit.io) para deploy rápido e gratuito.

1. Suba seu código para o GitHub (link acima).
2. Crie uma conta em Streamlit Cloud e conecte ao seu GitHub.
3. Crie um novo app, selecionando seu repositório e o arquivo steam_info.py.
4. Clique em Deploy.

---

## Estrutura do projeto

.
├── steam_info.py         # App principal
├── steam_api.py          # Módulo de acesso à API Steam
├── ui_renderer.py        # Funções de renderização da interface
├── requirements.txt      # Dependências Python
└── README.md             # Este arquivo

---

## Credenciais Steam

- Obtenha sua API Key em: https://steamcommunity.com/dev/apikey
- Seu Steam ID pode ser encontrado em: https://steamid.io

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

---

## Contato

Karel - [seu-email@example.com]

---

Divirta-se explorando seus jogos na Steam! 🎮
