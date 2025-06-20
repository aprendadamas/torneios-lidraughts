import requests
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

# Configurações
TOURNAMENT_API_URL = "https://lidraughts.org/api/tournament"
GAME_DOWNLOAD_URL = "https://lidraughts.org/api/tournament/{}/games"
OUTPUT_FILE = "index.html"
DAYS_TO_KEEP = 365

def get_finished_tournaments():
    """Busca torneios finalizados do Lidraughts."""
    tournaments = []
    try:
        response = requests.get(TOURNAMENT_API_URL, params={"status": "finished"})
        response.raise_for_status()
        tournaments = response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar torneios: {e}")
    return tournaments

def is_brazilian_tournament(tournament):
    """Verifica se o torneio é de damas brasileiras."""
    return tournament.get("variant", {}).get("key") == "brazilian"

def get_tournament_date(tournament):
    """Retorna a data de término do torneio."""
    try:
        end_date = datetime.fromtimestamp(tournament.get("endsAt", 0) / 1000)
        return end_date.date()
    except Exception as e:
        print(f"Erro ao parsear data do torneio {tournament.get('id')}: {e}")
        return None

def read_existing_html():
    """Lê o conteúdo atual do index.html, se existir."""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return None

def extract_tournaments_from_html(html_content):
    """Extrai torneios existentes do HTML para evitar duplicatas."""
    tournaments_by_date = defaultdict(list)
    if not html_content:
        return tournaments_by_date
    
    # Simples parsing para extrair seções de torneios (pode ser melhorado com regex ou parser HTML)
    lines = html_content.splitlines()
    current_date = None
    for line in lines:
        if '<h2>' in line and '</h2>' in line:
            # Ex.: <h2>2025-06-19</h2>
            date_str = line.split('>')[1].split('<')[0]
            try:
                current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                current_date = None
        elif '<li><a href="' in line and current_date:
            # Ex.: <li><a href="https://lidraughts.org/api/tournament/l7pCsRKp/games">Daily Brazilian Arena</a> (ID: l7pCsRKp)</li>
            parts = line.split('href="')[1].split('"')[0]
            tournament_id = parts.split('/')[-2]
            name = line.split('>')[2].split('<')[0]
            tournaments_by_date[current_date].append({
                "id": tournament_id,
                "name": name,
                "url": parts
            })
    
    return tournaments_by_date

def generate_html(tournaments_by_date):
    """Gera o novo conteúdo HTML com todos os torneios."""
    html_template_start = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Torneios Diários de Damas Brasileiras - Aprenda Damas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2 {
            color: #333;
        }
        .day-section {
            margin-bottom: 20px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 10px;
        }
        .tournament-list {
            list-style-type: none;
            padding: 0;
        }
        .tournament-list li {
            margin-bottom: 10px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .download-all {
            background-color: #0066cc;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
            margin-top: 10px;
        }
        .download-all:hover {
            background-color: #004c99;
            text-decoration: none;
        }
        .instructions {
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #0066cc;
            margin-bottom: 20px;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1>Torneios Diários de Damas Brasileiras - Lidraughts</h1>
    
    <div class="instructions">
        <h2>Como Baixar Partidas</h2>
        <p>Esta página lista os torneios de damas brasileiras realizados no Lidraughts nos últimos 365 dias. Clique nos links para baixar as partidas em formato PGN. Use um software de damas (ex.: Damas Brasil) para visualizar os jogos.</p>
        <p>Para encontrar torneios específicos, visite <a href="https://lidraughts.org/tournament" target="_blank">lidraughts.org/tournament</a>, clique na aba "Finished", e procure por torneios com "Brazilian" no nome. O ID do torneio está na URL (ex.: <code>abc123xy</code> em <code>https://lidraughts.org/tournament/abc123xy</code>).</p>
    </div>

    <div id="tournaments">
"""
    html_template_end = """    </div>

    <footer>
        <p>Atualizado diariamente por <a href="https://www.aprendadamas.org">Aprenda Damas</a>. Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a>.</p>
    </footer>
</body>
</html>
"""

    # Gera seções por dia
    sections = []
    today = datetime.now().date()
    cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
    
    for date in sorted(tournaments_by_date.keys(), reverse=True):
        if date < cutoff_date:
            continue
        section = f'        <div class="day-section">\n            <h2>{date}</h2>\n            <ul class="tournament-list">\n'
        for tournament in tournaments_by_date[date]:
            section += f'                <li><a href="{tournament["url"]}">{tournament["name"]}</a> (ID: {tournament["id"]})</li>\n'
        section += f'            </ul>\n            <a href="#" class="download-all">Baixar Todos (Em Breve)</a>\n        </div>'
        sections.append(section)
    
    # Combina tudo
    return html_template_start + "\n".join(sections) + html_template_end

def main():
    # Lê torneios existentes do HTML
    existing_html = read_existing_html()
    existing_tournaments = extract_tournaments_from_html(existing_html)
    
    # Busca novos torneios
    tournaments = get_finished_tournaments()
    new_tournaments_by_date = defaultdict(list)
    
    # Processa torneios brasileiros
    for tournament in tournaments:
        if not is_brazilian_tournament(tournament):
            continue
        date = get_tournament_date(tournament)
        if not date:
            continue
        tournament_id = tournament.get("id")
        name = tournament.get("fullName", "Torneio Sem Nome")
        url = GAME_DOWNLOAD_URL.format(tournament_id)
        
        # Evita duplicatas
        if any(t["id"] == tournament_id for t in existing_tournaments[date]):
            continue
        
        new_tournaments_by_date[date].append({
            "id": tournament_id,
            "name": name,
            "url": url
        })
    
    # Combina torneios existentes e novos
    for date in new_tournaments_by_date:
        existing_tournaments[date].extend(new_tournaments_by_date[date])
    
    # Gera novo HTML
    new_html = generate_html(existing_tournaments)
    
    # Salva o arquivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Arquivo {OUTPUT_FILE} atualizado com sucesso!")

if __name__ == "__main__":
    main()