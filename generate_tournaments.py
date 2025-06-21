import requests
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup
from collections import defaultdict

# Configurações
TOURNAMENT_PAGE_URL = "https://lidraughts.org/tournament"
OUTPUT_FILE = "index.html"
DAYS_TO_KEEP = 365

def get_tournament_page():
    """Faz o request para a página de torneios do Lidraughts."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(TOURNAMENT_PAGE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao acessar a página de torneios: {e}")
        return None

def extract_tournaments(html_content):
    """Extrai torneios 'Brazilian' da página HTML."""
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    tournaments = []
    for a in soup.select('a[href^="/tournament/"]'):
        text = a.get_text(strip=True)
        if "Brazilian" in text:
            url = "https://lidraughts.org" + a["href"]
            name = text.split("Brazilian")[0].strip()
            if name:
                tournaments.append({"name": name, "url": url})
                print(f"Torneio encontrado: {name} - {url}")
    print(f"Total de torneios encontrados: {len(tournaments)}")
    return tournaments

def has_games(tournament_url):
    """Verifica se o torneio tem jogos disponíveis."""
    tournament_id = tournament_url.split("/")[-1]
    game_url = f"https://lidraughts.org/api/tournament/{tournament_id}/games"
    try:
        response = requests.get(game_url, timeout=10)
        response.raise_for_status()
        content = response.text.strip()
        return len(content) > 0
    except requests.RequestException as e:
        print(f"Erro ao verificar jogos para {tournament_id}: {e}")
        return False

def read_existing_html():
    """Lê o conteúdo atual do index.html, se existir."""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return None

def extract_existing_tournaments(html_content):
    """Extrai torneios existentes do HTML para evitar duplicatas."""
    tournaments = {}
    if not html_content:
        return tournaments
    soup = BeautifulSoup(html_content, "html.parser")
    for li in soup.select('.tournament-list li'):
        a_tags = li.find_all('a')
        if len(a_tags) >= 2:
            tournament_url = a_tags[0]['href']
            download_url = a_tags[1]['href']
            name = a_tags[0].get_text(strip=True)
            tournaments[tournament_url] = {"name": name, "download_url": download_url}
    print(f"Torneios existentes encontrados: {len(tournaments)}")
    return tournaments

def generate_html(tournaments):
    """Gera o novo conteúdo HTML, preservando torneios existentes e adicionando novos."""
    today = datetime.now().strftime("%Y-%m-%d")
    existing_html = read_existing_html() or ""
    existing_tournaments = extract_existing_tournaments(existing_html)

    new_tournaments = []
    for tournament in tournaments:
        if has_games(tournament["url"]) and tournament["url"] not in existing_tournaments:
            tournament_id = tournament["url"].split("/")[-1]
            download_url = f"https://lidraughts.org/api/tournament/{tournament_id}/games"
            new_tournaments.append({"name": tournament["name"], "url": tournament["url"], "download_url": download_url})
            print(f"Novo torneio adicionado: {tournament['name']} - {tournament['url']}")

    if not existing_html:
        base_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Torneios Diários de Damas Brasileiras - Aprenda Damas</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1, h2 {{ color: #333; }}
        .day-section {{ margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        .tournament-list {{ list-style-type: none; padding: 0; }}
        .tournament-list li {{ margin-bottom: 10px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .download-all {{ background-color: #0066cc; color: white; padding: 8px 12px; border-radius: 4px; display: inline-block; margin-top: 10px; }}
        .download-all:hover {{ background-color: #004c99; text-decoration: none; }}
        .marketing {{ background-color: #25d366; color: white; padding: 10px; text-align: center; margin: 10px 0; border-radius: 5px; }}
        .marketing a {{ color: white; text-decoration: none; font-weight: bold; }}
        .marketing a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Torneios Diários de Damas Brasileiras - Lidraughts</h1>
    <div class="marketing">
        📱 <a href="https://wa.me/27988750076" target="_blank">Adquira o Programa Aurora Borealis - WhatsApp 27 98875-0076</a>
    </div>
    <div class="day-section">
        <h2>Atualizado em: {today}</h2>
        <ul class="tournament-list">
"""
    else:
        soup = BeautifulSoup(existing_html, "html.parser")
        day_section = soup.select_one('.day-section')
        if day_section:
            base_html = str(soup).rsplit('<div class="day-section"', 1)[0] + f'<div class="day-section"><h2>Atualizado em: {today}</h2><ul class="tournament-list">'
        else:
            base_html = existing_html.rsplit('<div class="day-section"', 1)[0] + f'<div class="day-section"><h2>Atualizado em: {today}</h2><ul class="tournament-list">'

    section = ""
    download_urls = []
    for url, data in existing_tournaments.items():
        section += f'            <li><a href="{url}">{data["name"]}</a> - <a href="{data["download_url"]}">Download</a></li>\n'
        download_urls.append(data["download_url"])
    for tournament in new_tournaments:
        section += f'            <li><a href="{tournament["url"]}">{tournament["name"]}</a> - <a href="{tournament["download_url"]}">Download</a></li>\n'
        download_urls.append(tournament["download_url"])
    if not section:
        section = "            <li>Nenhum torneio Brazilian com jogos disponíveis hoje.</li>\n"

    download_all_link = "#"
    if download_urls:
        download_all_link = ";".join(download_urls)

    new_html = base_html + section + f"""        </ul>
        <a href="{download_all_link}" class="download-all">Baixar Todos</a>
    </div>
    <footer>
        <p>Atualizado diariamente por <a href="https://www.aprendadamas.org">Aprenda Damas</a>. Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a>.</p>
    </footer>
</body>
</html>
"""
    print(f"Conteúdo gerado do index.html:\n{new_html}")
    return new_html

def main():
    html_content = get_tournament_page()
    if not html_content:
        print("Falha ao obter a página de torneios. Usando HTML existente.")
        html_content = read_existing_html() or ""
    tournaments = extract_tournaments(html_content)
    if not tournaments:
        print("Nenhum torneio Brazilian encontrado na página.")
    new_html = generate_html(tournaments)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Arquivo {OUTPUT_FILE} salvo com sucesso no caminho: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
