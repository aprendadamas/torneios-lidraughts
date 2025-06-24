import requests
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import time

# Configurações
TOURNAMENT_PAGE_URL = "https://lidraughts.org/tournament"
OUTPUT_FILE = "index.html"
DAYS_TO_KEEP = 365
MAX_PAGES = 50  # Limite máximo de páginas para evitar loops infinitos
REQUEST_DELAY = 5  # Atraso entre solicitações em segundos

def get_tournament_page():
    """Faz o request para a página de torneios do Lidraughts com paginação."""
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
    """Extrai torneios 'Brazilian' da página HTML, filtrando por data de hoje."""
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    tournaments = []
    today = datetime.now().strftime("%Y.%m.%d")  # Formato: 2025.06.23
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
            if name:
                tournaments.append({"name": name, "url": url, "date": date_elem})
                print(f"Torneio encontrado: {name} - {url} - Data: {date_elem}")
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
        .marketing a { color: white; text-decoration: none; font-weight: bold; }
        .marketing a:hover { text-decoration: underline; }
        .separator { background-color: #0066cc; color: white; padding: 10px; text-align: center; margin: 10px 0; border-radius: 5px; font-weight: bold; }
    </style>
    <script>
        function downloadSequentially(urls) {
            if (!urls || urls.length === 0) return;
            let index = 0;
            function downloadNext() {
                if (index >= urls.length) return;
                const link = document.createElement('a');
                link.href = urls[index];
                link.download = `tournament_${Date.now()}_${index}.pgn`; // Nome único para cada arquivo
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                index++;
                setTimeout(downloadNext, 2000); // Intervalo de 2 segundos entre downloads
            }
            downloadNext();
        }
    </script>
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

    section = ""
    download_urls = []
    # Adicionar torneios existentes
    for url, data in existing_tournaments.items():
        section += f'            <li><a href="{url}">{data["name"]}</a> - <a href="{data["download_url"]}">Download</a></li>\n'
        download_urls.append(data["download_url"])
    
    # Adicionar separador e novos torneios com link de download do dia
    today_download_urls = []
    if new_tournaments:
        section += f'        </ul><div class="separator">Torneios Atualizados Hoje - {today_date_only}</div><ul class="tournament-list">\n'
        for tournament in new_tournaments:
            section += f'            <li><a href="{tournament["url"]}">{tournament["name"]}</a> - <a href="{tournament["download_url"]}">Download</a></li>\n'
            download_urls.append(tournament["download_url"])
            today_download_urls.append(tournament["download_url"])
    elif not section:
        section = "            <li>Nenhum torneio Brazilian com jogos disponíveis hoje.</li>\n"

    download_all_link = "#"
    download_day_link = "#"
    if download_urls:
        download_all_link = ";".join(download_urls)
    if today_download_urls:
        download_day_link = ";".join(today_download_urls)

    new_html = base_html + section + f"""        </ul>
        <a href="{download_all_link}" class="download-all">Baixar Todos</a>
        {'<a href="#" class="download-day" onclick="downloadSequentially(\'{}\'.split(\';\'))">Baixar Todos do Dia</a>'.format(download_day_link) if today_download_urls else ''}
    </div>
    <footer>
        <p>Atualizado diariamente por <a href="https://www.aprendadamas.org">Aprenda Damas</a>. Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a>.</p>
    </footer>
</body>
</html>"""

    print(f"Conteúdo gerado do index.html:\n{new_html}")
    return new_html

def main():
    print(f"Iniciando execução em: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
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
