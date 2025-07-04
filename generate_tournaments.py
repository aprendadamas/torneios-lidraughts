import requests
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import re
import json

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
            print(f"Erro HTTP ao acessar a página {url}: {e} (Status: {response.status_code})")
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

def extract_existing_tournaments_by_date(html_content):
    """Extrai torneios existentes organizados por data."""
    tournaments_by_date = defaultdict(list)
    if not html_content:
        return tournaments_by_date
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Procurar por todas as seções de dia
    day_sections = soup.select('.day-section')
    
    for section in day_sections:
        # Extrair a data do h2
        date_h2 = section.find('h2')
        if date_h2:
            date_text = date_h2.get_text(strip=True)
            # Extrair apenas a data (YYYY-MM-DD)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                date = date_match.group(1)
                
                # Extrair todos os torneios dessa seção
                for li in section.select('.tournament-list li'):
                    a_tags = li.find_all('a')
                    if len(a_tags) >= 2:
                        tournament_url = a_tags[0]['href']
                        download_url = a_tags[1]['href']
                        name = a_tags[0].get_text(strip=True)
                        tournaments_by_date[date].append({
                            "name": name,
                            "url": tournament_url,
                            "download_url": download_url
                        })
    
    return tournaments_by_date

def generate_html(tournaments):
    """Gera o novo conteúdo HTML com separador por dia e opção de download diário."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler HTML existente e extrair torneios por data
    existing_html = read_existing_html()
    existing_tournaments_by_date = extract_existing_tournaments_by_date(existing_html)
    
    # Adicionar novos torneios ao dia de hoje
    new_tournaments = []
    for tournament in tournaments:
        if has_games(tournament["url"]):
            tournament_id = tournament["url"].split("/")[-1]
            download_url = f"https://lidraughts.org/api/tournament/{tournament_id}/games"
            new_tournaments.append({
                "name": tournament["name"],
                "url": tournament["url"],
                "download_url": download_url
            })
            print(f"Novo torneio adicionado: {tournament['name']} - {tournament['url']}")
    
    # Adicionar novos torneios à data de hoje
    if new_tournaments:
        if today_str in existing_tournaments_by_date:
            # Verificar duplicatas
            existing_urls = {t["url"] for t in existing_tournaments_by_date[today_str]}
            for new_t in new_tournaments:
                if new_t["url"] not in existing_urls:
                    existing_tournaments_by_date[today_str].append(new_t)
        else:
            existing_tournaments_by_date[today_str] = new_tournaments
    
    # Remover datas antigas (mais de DAYS_TO_KEEP dias)
    cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
    dates_to_remove = []
    for date_str in existing_tournaments_by_date.keys():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj < cutoff_date:
            dates_to_remove.append(date_str)
    
    for date_str in dates_to_remove:
        del existing_tournaments_by_date[date_str]
    
    # Ordenar datas (mais recente primeiro)
    sorted_dates = sorted(existing_tournaments_by_date.keys(), reverse=True)
    
    # Gerar HTML
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Torneios Diários de Damas Brasileiras - Aprenda Damas</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1, h2 {{ color: #333; }}
        .day-section {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; background-color: #f9f9f9; }}
        .day-section h2 {{ margin-top: 0; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        .tournament-list {{ list-style-type: none; padding: 0; }}
        .tournament-list li {{ margin-bottom: 10px; padding: 5px; background-color: white; border-radius: 3px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .download-day {{ background-color: #28a745; color: white; padding: 8px 15px; border-radius: 4px; display: inline-block; margin-top: 10px; font-weight: bold; }}
        .download-day:hover {{ background-color: #218838; text-decoration: none; }}
        .marketing {{ background-color: #25d366; color: white; padding: 15px; text-align: center; margin: 20px 0; border-radius: 5px; }}
        .marketing a {{ color: white; text-decoration: none; font-weight: bold; font-size: 1.1em; }}
        .marketing a:hover {{ text-decoration: underline; }}
        .update-info {{ background-color: #17a2b8; color: white; padding: 10px; text-align: center; margin: 10px 0; border-radius: 5px; }}
        .stats {{ margin: 10px 0; font-size: 0.9em; color: #666; }}
    </style>
    <script>
        function downloadAllFromDay(date, urls) {{
            const urlList = urls.split(';');
            let index = 0;
            
            function downloadNext() {{
                if (index < urlList.length) {{
                    const link = document.createElement('a');
                    link.href = urlList[index];
                    link.download = '';
                    link.style.display = 'none';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    index++;
                    // Aguardar 1 segundo entre downloads
                    setTimeout(downloadNext, 1000);
                }}
            }}
            
            if (confirm(`Deseja baixar ${{urlList.length}} torneios do dia ${{date}}?`)) {{
                downloadNext();
            }}
        }}
    </script>
</head>
<body>
    <h1>🎯 Torneios Diários de Damas Brasileiras - Lidraughts</h1>
    
    <div class="marketing">
        📱 <a href="https://wa.me/27988750076" target="_blank">Adquira o Programa Aurora Borealis - WhatsApp (27) 98875-0076</a>
    </div>
    
    <div class="update-info">
        🔄 Última atualização: {today_datetime} | 🏆 Top 5 torneios com mais participantes por dia
    </div>
"""
    
    # Adicionar seções por dia
    for date_str in sorted_dates:
        tournaments_list = existing_tournaments_by_date[date_str]
        if not tournaments_list:
            continue
            
        # Formatar data para exibição
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        weekday = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][date_obj.weekday()]
        
        # Criar lista de URLs para download
        download_urls = ";".join([t["download_url"] for t in tournaments_list])
        
        html_content += f"""
    <div class="day-section">
        <h2>📅 {weekday}, {formatted_date}</h2>
        <div class="stats">Total de torneios: {len(tournaments_list)}</div>
        <ul class="tournament-list">
"""
        
        for tournament in tournaments_list:
            name = tournament["name"]
            # Se o nome for apenas a URL, tentar extrair um nome melhor
            if name.startswith("https://"):
                name = f"Torneio {tournament['url'].split('/')[-1]}"
            
            html_content += f"""            <li>🏁 <a href="{tournament['url']}">{name}</a> - <a href="{tournament['download_url']}">📥 Download Individual</a></li>
"""
        
        html_content += f"""        </ul>
        <button class="download-day" onclick="downloadAllFromDay('{formatted_date}', '{download_urls}')">
            📥 Baixar Todos os {len(tournaments_list)} Torneios deste Dia
        </button>
    </div>
"""
    
    html_content += """
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; text-align: center; color: #666;">
        <p>🎯 Atualizado diariamente às 00:00 por <a href="https://www.aprendadamas.org">Aprenda Damas</a></p>
        <p>📊 Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a></p>
    </footer>
</body>
</html>"""
    
    # Salvar o arquivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Arquivo {OUTPUT_FILE} atualizado com sucesso!")

def main():
    """Função principal."""
    print("=== TESTE: Script iniciado com sucesso! ===")  # Adicione esta linha
    print("Iniciando coleta de torneios...")
    html_content = get_tournament_page()
    if html_content:
        tournaments = extract_tournaments(html_content)
        if tournaments:
            generate_html(tournaments)
        else:
            print("Nenhum torneio 'Brazilian' encontrado.")
    else:
        print("Erro ao buscar a página de torneios.")

if __name__ == "__main__":
    main()
