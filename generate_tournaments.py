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
DAYS_TO_KEEP = 30  # Manter histórico de 30 dias
TOP_TOURNAMENTS = 10  # Número de torneios com mais participantes a serem selecionados
REQUEST_DELAY = 2  # Atraso entre solicitações em segundos

def get_tournament_page():
    """Faz o request para a página principal de torneios do Lidraughts."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Acessando {TOURNAMENT_PAGE_URL}...")
        response = requests.get(TOURNAMENT_PAGE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

def extract_brazilian_tournaments(html_content):
    """Extrai torneios 'Brazilian' e seus números de participantes."""
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, "html.parser")
    tournaments = []
    
    # Procurar por todas as linhas de torneio
    tournament_rows = soup.find_all('a', href=re.compile(r'/tournament/'))
    
    for link in tournament_rows:
        # Verificar se é um torneio brasileiro
        row_text = link.get_text(strip=True)
        if 'Brazilian' in row_text:
            # Pegar o container pai que contém todas as informações
            parent = link.parent
            while parent and not parent.find_all(string=re.compile(r'\d+$')):
                parent = parent.parent
            
            if parent:
                # Extrair informações
                tournament_url = "https://lidraughts.org" + link['href']
                tournament_id = link['href'].split('/')[-1]
                
                # Extrair nome do torneio
                tournament_name = link.get_text(strip=True)
                
                # Procurar pelo número de participantes (último número na linha)
                full_text = parent.get_text()
                numbers = re.findall(r'\b\d+\b', full_text)
                
                if numbers:
                    # O último número geralmente é o número de participantes
                    participants = int(numbers[-1])
                    
                    tournaments.append({
                        'name': tournament_name,
                        'url': tournament_url,
                        'id': tournament_id,
                        'participants': participants
                    })
                    
                    print(f"Encontrado: {tournament_name} - {participants} participantes")
    
    # Ordenar por número de participantes e pegar os TOP
    tournaments.sort(key=lambda x: x['participants'], reverse=True)
    top_tournaments = tournaments[:TOP_TOURNAMENTS]
    
    print(f"\nTotal de torneios Brazilian encontrados: {len(tournaments)}")
    print(f"Selecionados os {len(top_tournaments)} com mais participantes")
    
    return top_tournaments

def has_games(tournament_id):
    """Verifica se o torneio tem jogos disponíveis."""
    game_url = f"https://lidraughts.org/api/tournament/{tournament_id}/games"
    try:
        response = requests.head(game_url, timeout=5)
        return response.status_code == 200
    except:
        return True  # Assumir que tem jogos em caso de erro

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
            # Extrair apenas a data (DD/MM/YYYY)
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_text)
            if date_match:
                date_display = date_match.group(1)
                # Converter para formato YYYY-MM-DD para armazenamento
                day, month, year = date_display.split('/')
                date = f"{year}-{month}-{day}"
                
                # Extrair todos os torneios dessa seção
                for li in section.select('.tournament-list li'):
                    a_tags = li.find_all('a')
                    if len(a_tags) >= 2:
                        tournament_url = a_tags[0]['href']
                        download_url = a_tags[1]['href']
                        name = a_tags[0].get_text(strip=True).replace('🏁 ', '')
                        tournaments_by_date[date].append({
                            "name": name,
                            "url": tournament_url,
                            "download_url": download_url
                        })
    
    return tournaments_by_date

def generate_html(new_tournaments):
    """Gera o novo conteúdo HTML com separador por dia e opção de download diário."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler HTML existente e extrair torneios por data
    existing_html = read_existing_html()
    existing_tournaments_by_date = extract_existing_tournaments_by_date(existing_html)
    
    # Adicionar novos torneios ao dia de hoje
    tournaments_to_add = []
    for tournament in new_tournaments:
        if has_games(tournament["id"]):
            download_url = f"https://lidraughts.org/api/tournament/{tournament['id']}/games"
            tournaments_to_add.append({
                "name": tournament["name"],
                "url": tournament["url"],
                "download_url": download_url
            })
            print(f"Adicionando: {tournament['name']} ({tournament['participants']} participantes)")
        else:
            print(f"Pulando (sem jogos): {tournament['name']}")
    
    # Adicionar novos torneios à data de hoje
    if tournaments_to_add:
        if today_str in existing_tournaments_by_date:
            # Verificar duplicatas
            existing_urls = {t["url"] for t in existing_tournaments_by_date[today_str]}
            added_count = 0
            for new_t in tournaments_to_add:
                if new_t["url"] not in existing_urls:
                    existing_tournaments_by_date[today_str].append(new_t)
                    added_count += 1
                else:
                    print(f"Torneio já existe: {new_t['name']}")
            print(f"Adicionados {added_count} novos torneios ao dia de hoje")
        else:
            existing_tournaments_by_date[today_str] = tournaments_to_add
            print(f"Criada nova entrada para hoje com {len(tournaments_to_add)} torneios")
    
    # Remover datas antigas (mais de DAYS_TO_KEEP dias)
    cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
    dates_to_remove = []
    for date_str in existing_tournaments_by_date.keys():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj < cutoff_date:
                dates_to_remove.append(date_str)
        except:
            continue
    
    for date_str in dates_to_remove:
        del existing_tournaments_by_date[date_str]
        print(f"Removida data antiga: {date_str}")
    
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
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; background-color: #f5f5f5; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; color: #7f8c8d; margin-bottom: 30px; }}
        .day-section {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 8px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .day-section h2 {{ margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .tournament-list {{ list-style-type: none; padding: 0; }}
        .tournament-list li {{ margin-bottom: 12px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }}
        .tournament-list li:hover {{ background-color: #e9ecef; }}
        .tournament-name {{ flex-grow: 1; }}
        a {{ color: #3498db; text-decoration: none; font-weight: 500; }}
        a:hover {{ text-decoration: underline; }}
        .download-link {{ color: #27ae60; font-size: 0.9em; }}
        .download-day {{ background-color: #27ae60; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 15px; font-weight: bold; border: none; cursor: pointer; }}
        .download-day:hover {{ background-color: #229954; text-decoration: none; }}
        .marketing {{ background-color: #25d366; color: white; padding: 15px; text-align: center; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .marketing a {{ color: white; text-decoration: none; font-weight: bold; font-size: 1.1em; }}
        .marketing a:hover {{ text-decoration: underline; }}
        .update-info {{ background-color: #3498db; color: white; padding: 12px; text-align: center; margin: 15px 0; border-radius: 8px; }}
        .stats {{ margin: 10px 0; font-size: 0.9em; color: #7f8c8d; }}
        .no-tournaments {{ text-align: center; padding: 40px; color: #7f8c8d; }}
        footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; }}
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
    <h1>🎯 Torneios Diários de Damas Brasileiras</h1>
    <p class="subtitle">Os {TOP_TOURNAMENTS} torneios com mais participantes do Lidraughts</p>
    
    <div class="marketing">
        📱 <a href="https://wa.me/27988750076" target="_blank">Adquira o Programa Aurora Borealis - WhatsApp (27) 98875-0076</a>
    </div>
    
    <div class="update-info">
        🔄 Última atualização: {today_datetime} | 🏆 Atualizado diariamente às 00:00
    </div>
"""
    
    if not sorted_dates:
        html_content += """
    <div class="no-tournaments">
        <p>Nenhum torneio disponível no momento.</p>
        <p>Novos torneios serão adicionados automaticamente!</p>
    </div>
"""
    else:
        # Adicionar seções por dia
        for date_str in sorted_dates:
            tournaments_list = existing_tournaments_by_date[date_str]
            if not tournaments_list:
                continue
                
            # Formatar data para exibição
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
                weekday = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][date_obj.weekday()]
                
                # Verificar se é hoje
                if date_str == today_str:
                    date_label = f"HOJE - {weekday}, {formatted_date}"
                else:
                    date_label = f"{weekday}, {formatted_date}"
            except:
                date_label = date_str
            
            # Criar lista de URLs para download
            download_urls = ";".join([t["download_url"] for t in tournaments_list])
            
            html_content += f"""
    <div class="day-section">
        <h2>📅 {date_label}</h2>
        <div class="stats">Total de torneios: {len(tournaments_list)}</div>
        <ul class="tournament-list">
"""
            
            for tournament in tournaments_list:
                name = tournament["name"]
                html_content += f"""            <li>
                <span class="tournament-name">🏁 <a href="{tournament['url']}">{name}</a></span>
                <a href="{tournament['download_url']}" class="download-link">📥 Baixar</a>
            </li>
"""
            
            html_content += f"""        </ul>
        <button class="download-day" onclick="downloadAllFromDay('{formatted_date}', '{download_urls}')">
            📥 Baixar Todos os {len(tournaments_list)} Torneios deste Dia
        </button>
    </div>
"""
    
    html_content += """
    <footer>
        <p>🎯 Desenvolvido por <a href="https://www.aprendadamas.org">Aprenda Damas</a></p>
        <p>📊 Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a></p>
        <p>💡 Dica: Os torneios são selecionados automaticamente com base no número de participantes</p>
    </footer>
</body>
</html>"""
    
    # Salvar o arquivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n✅ Arquivo {OUTPUT_FILE} atualizado com sucesso!")

def main():
    """Função principal."""
    print("=== Iniciando coleta de torneios ===")
    print(f"Data/hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Buscando os {TOP_TOURNAMENTS} torneios Brazilian com mais participantes...\n")
    
    # Buscar página de torneios
    html_content = get_tournament_page()
    
    if html_content:
        # Extrair torneios brasileiros
        tournaments = extract_brazilian_tournaments(html_content)
        
        if tournaments:
            print(f"\n✅ Encontrados {len(tournaments)} torneios para processar")
            generate_html(tournaments)
        else:
            print("\n⚠️ Nenhum torneio Brazilian encontrado na página")
            # Ainda assim, gerar HTML para manter o histórico
            generate_html([])
    else:
        print("\n❌ Erro ao buscar a página de torneios")

if __name__ == "__main__":
    main()
