import requests
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import re

# Configurações
TOURNAMENT_PAGE_URL = "https://lidraughts.org/tournament"
OUTPUT_FILE = "index.html"
DAYS_TO_KEEP = 365
MAX_PAGES = 19  # Limite máximo de páginas para evitar o erro na página 20
REQUEST_DELAY = 5  # Atraso entre solicitações em segundos
TOP_TOURNAMENTS = 5  # Número de torneios com mais participantes a serem selecionados

def get_tournament_page():
    """Faz o request para a página de torneios do Lidraughts com paginação limitada a 19 páginas."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    all_content = ""
    page = 1
    while page <= MAX_PAGES:
        url = f"{TOURNAMENT_PAGE_URL}?page={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            tournament_links = soup.select('a[href^="/tournament/"]')
            if not tournament_links or "No tournaments found" in content:
                print(f"Nenhum torneio encontrado na página {page}. Parando.")
                break
            all_content += content
            print(f"Processando página {page}...")
            page += 1
            time.sleep(REQUEST_DELAY)
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao acessar a página {url}: {e} (Status: {response.status_code}, Conteúdo: {response.text[:100]})")
            break
        except requests.RequestException as e:
            print(f"Erro ao acessar a página {url}: {e}")
            break
        except Exception as e:
            print(f"Erro inesperado na página {page}: {e}")
            break
    return all_content if all_content else None

def extract_tournaments(html_content):
    """Extrai torneios 'Brazilian' e seleciona os 5 com mais participantes dentro das 19 páginas."""
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    tournaments = []
    today = datetime.now().strftime("%Y.%m.%d")  # Formato: 2025.06.24
    for a in soup.select('a[href^="/tournament/"]'):
        text = a.get_text(strip=True)
        if "Brazilian" in text:
            parent = a.find_parent('div', class_=lambda x: x and 'event__header' in x)
            date_elem = None
            if parent:
                date_elem = parent.find(string=lambda t: t and any(d in t for d in [today, "Today"]))
            if not date_elem:
                print(f"Data não encontrada para torneio: {text} - {a['href']}. Usando fallback para hoje.")
                date_elem = today
            url = "https://lidraughts.org" + a["href"]
            name = text.split("Brazilian")[0].strip() or text
            # Extrair o número de participantes do texto do parent
            participants = 0
            if parent:
                full_text = parent.get_text(strip=True)
                # Usar regex para pegar o último número da linha
                match = re.search(r'\d+$', full_text)
                if match:
                    participants = int(match.group())
            if name and participants > 0:
                tournaments.append({"name": name, "url": url, "date": date_elem, "participants": participants})
                print(f"Torneio encontrado: {name} - {url} - Data: {date_elem} - Participantes: {participants}")
    print(f"Total de torneios 'Brazilian' encontrados nas 19 páginas: {len(tournaments)}")
    
    # Ordenar por número de participantes e selecionar os 5 primeiros
    if tournaments:
        tournaments_sorted = sorted(tournaments, key=lambda x: x["participants"], reverse=True)[:TOP_TOURNAMENTS]
        print(f"Selecionados os {TOP_TOURNAMENTS} torneios com mais participantes: {[t['name'] for t in tournaments_sorted]}")
        return tournaments_sorted
    return []

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
    """Gera o novo conteúdo HTML com separador e opção de download sequencial do dia."""
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_date_only = datetime.now().strftime("%Y-%m-%d")
    existing_html = read_existing_html() or ""
    existing_tournaments = extract_existing_tournaments(existing_html)

    new_tournaments = []
    for tournament in tournaments:
        if has_games(tournament["url"]) and tournament["url"] not in existing_tournaments:
            tournament_id = tournament["url"].split("/")[-1]
            download_url = f"https://lidraughts.org/api/tournament/{tournament_id}/games"
            new_tournaments.append({"name": tournament["name"], "url": tournament["url"], "download_url": download_url})
            print(f"Novo torneio adicionado: {tournament['name']} - {tournament['url']}")

    # Construir o HTML completo
    base_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Torneios Diários de Damas Brasileiras - Aprenda Damas</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        h1, h2 { color: #333; }
        .day-section { margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
        .tournament-list { list-style-type: none; padding: 0; }
        .tournament-list li { margin-bottom: 10px; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .download-all, .download-day { background-color: #0066cc; color: white; padding: 8px 12px; border-radius: 4px; display: inline-block; margin-top: 10px; }
        .download-all:hover, .download-day:hover { background-color: #004c99; text-decoration: none; }
        .marketing { background-color: #25d366; color: white; padding: 10px; text-align: center; margin: 10px 0; border-radius: 5px; }
        .marketing
