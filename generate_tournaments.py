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
DAYS_TO_KEEP = 365  # Manter histórico de 365 dias
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
        print(f"✅ Página carregada com sucesso! Status: {response.status_code}")
        print(f"   Tamanho do conteúdo: {len(response.text)} caracteres")
        return response.text
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar a página: {e}")
        return NoneUser-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
    
    # Torneios especiais que devemos ignorar
    SPECIAL_TOURNAMENTS = ['Monthly Brazilian', 'Brazilian Shield', 'Yearly Brazilian', 'Weekly Brazilian']
    
    # Procurar por todas as linhas de torneio
    tournament_rows = soup.find_all('a', href=re.compile(r'/tournament/'))
    
    for link in tournament_rows:
        # Verificar se é um torneio brasileiro
        row_text = link.get_text(strip=True)
        if 'Brazilian' in row_text:
            # Pular torneios especiais
            skip = False
            for special in SPECIAL_TOURNAMENTS:
                if special in row_text:
                    print(f"Pulando torneio especial: {row_text}")
                    skip = True
                    break
            
            if skip:
                continue
            
            # Pular se o nome termina com hífen (torneio inativo)
            if row_text.strip().endswith('-'):
                print(f"Pulando torneio inativo: {row_text}")
                continue
            
            # Pegar o container pai que contém todas as informações
            parent = link.parent
            while parent and not parent.find_all(string=re.compile(r'\d+

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
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"\n📖 Arquivo {OUTPUT_FILE} existente lido com sucesso")
            print(f"   Tamanho: {len(content)} caracteres")
            
            # Verificar se tem torneios especiais no conteúdo
            special_count = 0
            for special in ['Monthly Brazilian-', 'Brazilian Shield-', 'Yearly Brazilian-']:
                special_count += content.count(special)
            if special_count > 0:
                print(f"   ⚠️ Encontrados {special_count} torneios especiais no HTML existente")
                
            return content
        except Exception as e:
            print(f"\n❌ Erro ao ler {OUTPUT_FILE}: {e}")
            return None
    else:
        print(f"\n📖 Arquivo {OUTPUT_FILE} não existe, será criado um novo")
        return None

def extract_existing_tournaments_by_date(html_content):
    """Extrai torneios existentes organizados por data."""
    tournaments_by_date = defaultdict(list)
    if not html_content:
        return tournaments_by_date
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Primeiro, tentar extrair do formato novo (com day-section)
    day_sections = soup.select('.day-section')
    
    if day_sections:
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
    else:
        # Se não encontrar day-sections, tentar formato antigo
        print("   Formato antigo detectado, tentando extrair torneios...")
        
        # Procurar pela data real no conteúdo HTML
        # Primeiro tentar encontrar "Última atualização:" no update-info
        update_info = soup.find('div', class_='update-info')
        date = None
        
        if update_info:
            update_text = update_info.get_text()
            # Procurar por data no formato YYYY-MM-DD
            date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', update_text)
            if date_match:
                date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                print(f"   Data encontrada no update-info: {date}")
        
        # Se ainda não tiver data, procurar no h2 antigo
        if not date:
            update_h2 = soup.find('h2', string=re.compile(r'Atualizado em:'))
            if update_h2:
                text = update_h2.get_text()
                date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
                if date_match:
                    date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                    print(f"   Data encontrada no h2: {date}")
        
        # Se ainda não tiver data, usar ontem como fallback
        if not date:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"   Nenhuma data encontrada, usando ontem: {date}")
        
        # Procurar pela lista de torneios
        # Tentar primeiro dentro de day-section (novo formato que pode ter apenas uma seção)
        day_section = soup.find('div', class_='day-section')
        if day_section:
            tournament_list = day_section.select('.tournament-list li')
        else:
            # Formato mais antigo
            tournament_list = soup.select('.tournament-list li')
        
        if tournament_list:
            print(f"   Encontrados {len(tournament_list)} torneios na lista")
            # Extrair todos os torneios
            for li in tournament_list:
                a_tags = li.find_all('a')
                if len(a_tags) >= 2:
                    tournament_url = a_tags[0]['href']
                    download_url = a_tags[1]['href'] 
                    name = a_tags[0].get_text(strip=True).replace('🏁 ', '')
                    
                    # Não adicionar torneios especiais ao histórico
                    if not any(special in name for special in ['Monthly Brazilian', 'Brazilian Shield', 'Yearly Brazilian', 'Weekly Brazilian']):
                        if not name.strip().endswith('-'):
                            tournaments_by_date[date].append({
                                "name": name,
                                "url": tournament_url,
                                "download_url": download_url
                            })
            
            if tournaments_by_date[date]:
                print(f"   Migrados {len(tournaments_by_date[date])} torneios válidos do formato antigo para {date}")
            else:
                print(f"   Nenhum torneio válido encontrado após filtrar torneios especiais")
    
    return tournaments_by_date

def clean_special_tournaments(tournaments_by_date):
    """Remove torneios especiais (Monthly, Shield, Yearly) do histórico."""
    SPECIAL_TOURNAMENTS = ['Monthly Brazilian', 'Brazilian Shield', 'Yearly Brazilian', 'Weekly Brazilian']
    
    cleaned_count = 0
    for date in tournaments_by_date:
        original_count = len(tournaments_by_date[date])
        # Filtrar torneios, removendo os especiais
        tournaments_by_date[date] = [
            t for t in tournaments_by_date[date] 
            if not any(special in t['name'] for special in SPECIAL_TOURNAMENTS)
            and not t['name'].strip().endswith('-')
        ]
        removed = original_count - len(tournaments_by_date[date])
        if removed > 0:
            cleaned_count += removed
            print(f"   Removidos {removed} torneios especiais de {date}")
    
    if cleaned_count > 0:
        print(f"\n🧹 Limpeza: removidos {cleaned_count} torneios especiais do histórico")
    
    return tournaments_by_date

def generate_html(new_tournaments):
    """Gera o novo conteúdo HTML com separador por dia e opção de download diário."""
    print("\n=== Gerando HTML ===")
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler HTML existente e extrair torneios por data
    existing_html = read_existing_html()
    existing_tournaments_by_date = extract_existing_tournaments_by_date(existing_html)
    
    # IMPORTANTE: Limpar torneios especiais do histórico
    if existing_tournaments_by_date:
        print("\n🧹 Limpando torneios especiais do histórico...")
        existing_tournaments_by_date = clean_special_tournaments(existing_tournaments_by_date)
    
    # Debug: mostrar quantos dias de histórico temos
    if existing_tournaments_by_date:
        total_existing = sum(len(tournaments) for tournaments in existing_tournaments_by_date.values())
        print(f"\n📚 Histórico após limpeza: {len(existing_tournaments_by_date)} dias, {total_existing} torneios total")
        if existing_tournaments_by_date:
            oldest_date = min(existing_tournaments_by_date.keys())
            newest_date = max(existing_tournaments_by_date.keys())
            print(f"   Período: {oldest_date} até {newest_date}")
    else:
        print("\n📚 Nenhum histórico válido após limpeza")
    
    # Adicionar novos torneios ao dia de hoje
    if new_tournaments:
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
    else:
        print("\n⚠️ Nenhum torneio novo para adicionar hoje, mantendo histórico existente")
    
    # Remover datas antigas (mais de DAYS_TO_KEEP dias) e datas sem torneios
    cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
    dates_to_remove = []
    for date_str in existing_tournaments_by_date.keys():
        try:
            # Remover se não tiver torneios
            if not existing_tournaments_by_date[date_str]:
                dates_to_remove.append(date_str)
                continue
                
            # Remover se for muito antiga
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj < cutoff_date:
                dates_to_remove.append(date_str)
        except:
            # Se não conseguir processar a data, não remover
            print(f"⚠️ Não foi possível processar a data: {date_str}")
            continue
    
    if dates_to_remove:
        print(f"\n🗑️ Removendo {len(dates_to_remove)} datas (antigas ou vazias)")
        for date_str in dates_to_remove:
            reason = "vazia" if not existing_tournaments_by_date[date_str] else f"antiga (mais de {DAYS_TO_KEEP} dias)"
            del existing_tournaments_by_date[date_str]
            print(f"   Removida: {date_str} ({reason})")
    else:
        print(f"\n✅ Nenhuma data para remover")
    
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
    <!-- Cache buster: {datetime.now().timestamp()} -->
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
            
            # Criar lista de URLs para download (apenas torneios válidos)
            valid_tournaments = []
            for t in tournaments_list:
                if not any(special in t["name"] for special in ['Monthly Brazilian', 'Brazilian Shield', 'Yearly Brazilian', 'Weekly Brazilian']):
                    if not t["name"].strip().endswith('-'):
                        valid_tournaments.append(t)
            
            download_urls = ";".join([t["download_url"] for t in valid_tournaments])
            actual_count = len(valid_tournaments)
            
            html_content += f"""
    <div class="day-section">
        <h2>📅 {date_label}</h2>
        <div class="stats">Total de torneios: {actual_count}</div>
        <ul class="tournament-list">
"""
            
            for tournament in tournaments_list:
                name = tournament["name"]
                # Verificação final: pular torneios especiais que possam ter passado
                if any(special in name for special in ['Monthly Brazilian', 'Brazilian Shield', 'Yearly Brazilian', 'Weekly Brazilian']):
                    continue
                if name.strip().endswith('-'):
                    continue
                    
                html_content += f"""            <li>
                <span class="tournament-name">🏁 <a href="{tournament['url']}">{name}</a></span>
                <a href="{tournament['download_url']}" class="download-link">📥 Baixar</a>
            </li>
"""
            
            html_content += f"""        </ul>
        <button class="download-day" onclick="downloadAllFromDay('{formatted_date}', '{download_urls}')">
            📥 Baixar Todos os {actual_count} Torneios deste Dia
        </button>
    </div>
"""
    
    html_content += """
    <footer>
        <p>🎯 Desenvolvido por <a href="https://www.aprendadamas.org">Aprenda Damas</a></p>
        <p>📊 Dados fornecidos por <a href="https://lidraughts.org">Lidraughts.org</a></p>
        <p>💡 Dica: Os torneios são selecionados automaticamente com base no número de participantes</p>
        <p>📅 Histórico mantido por até 365 dias</p>
    </footer>
</body>
</html>"""
    
    # Salvar o arquivo
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Verificar se o arquivo foi salvo
        if os.path.exists(OUTPUT_FILE):
            file_size = os.path.getsize(OUTPUT_FILE)
            print(f"\n✅ Arquivo {OUTPUT_FILE} salvo com sucesso!")
            print(f"   Tamanho do arquivo: {file_size} bytes")
        else:
            print(f"\n❌ ERRO: Arquivo {OUTPUT_FILE} não foi criado!")
            
    except Exception as e:
        print(f"\n❌ ERRO ao salvar arquivo: {e}")
        return
    
    # Resumo final
    total_tournaments = sum(len(tournaments) for tournaments in existing_tournaments_by_date.values())
    print(f"📊 Resumo: {len(existing_tournaments_by_date)} dias de histórico, {total_tournaments} torneios total")

def main():
    """Função principal."""
    print("=== Iniciando coleta de torneios ===")
    print(f"Data/hora atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Buscando os {TOP_TOURNAMENTS} torneios Brazilian com mais participantes...\n")
    
    # Buscar página de torneios
    html_content = get_tournament_page()
    
    if html_content:
        # Extrair torneios brasileiros
        tournaments = extract_brazilian_tournaments(html_content)
        
        if tournaments:
            print(f"\n✅ Encontrados {len(tournaments)} torneios para processar")
        else:
            print("\n⚠️ Nenhum torneio Brazilian válido encontrado na página")
            print("   (torneios especiais e inativos foram ignorados)")
        
        # Sempre gerar HTML para manter o histórico
        generate_html(tournaments)
    else:
        print("\n❌ Erro ao buscar a página de torneios")

if __name__ == "__main__":
    try:
        main()
        print("\n=== Script finalizado com sucesso! ===")
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        
        # Tentar salvar um HTML de erro
        try:
            error_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Erro - Torneios Diários</title>
</head>
<body>
    <h1>Erro ao processar torneios</h1>
    <p>Ocorreu um erro: {str(e)}</p>
    <p>Por favor, verifique os logs.</p>
</body>
</html>"""
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(error_html)
            print(f"\n⚠️ HTML de erro salvo em {OUTPUT_FILE}")
        except:
            print("\n❌ Não foi possível salvar nem mesmo o HTML de erro!")
        
        # Sair com código de erro
        import sys
        sys.exit(1)
)):
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
                    
                    # Só adicionar se tiver pelo menos 1 participante
                    if participants > 0:
                        tournaments.append({
                            'name': tournament_name,
                            'url': tournament_url,
                            'id': tournament_id,
                            'participants': participants
                        })
                        
                        print(f"Encontrado: {tournament_name} - {participants} participantes")
                    else:
                        print(f"Pulando (sem participantes): {tournament_name}")
    
    # Ordenar por número de participantes e pegar os TOP
    tournaments.sort(key=lambda x: x['participants'], reverse=True)
    top_tournaments = tournaments[:TOP_TOURNAMENTS]
    
    print(f"\nTotal de torneios Brazilian válidos encontrados: {len(tournaments)}")
    if tournaments:
        print(f"Selecionados os {len(top_tournaments)} com mais participantes:")
        for t in top_tournaments:
            print(f"  - {t['name']}: {t['participants']} participantes")
    
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
    
    # Primeiro, tentar extrair do formato novo (com day-section)
    day_sections = soup.select('.day-section')
    
    if day_sections:
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
    else:
        # Se não encontrar day-sections, tentar formato antigo
        # Procurar pela lista de torneios antiga
        tournament_list = soup.select('.tournament-list li')
        if tournament_list:
            # Todos os torneios antigos vão para uma data padrão
            # Vamos usar a data do último update se disponível
            update_h2 = soup.find('h2', string=re.compile(r'Atualizado em:'))
            if update_h2:
                # O formato no HTML antigo é "2025-06-24" mas parece ser dia 24 de junho
                # Vamos procurar especificamente por 2025-06-24
                text = update_h2.get_text()
                if "2025-06-24" in text:
                    # Converter para o formato correto (24 de junho de 2025)
                    date = "2025-06-24"
                else:
                    # Procurar por data no formato YYYY-MM-DD
                    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
                    if date_match:
                        date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                    else:
                        # Usar ontem como fallback
                        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                # Usar ontem como fallback
                date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Extrair todos os torneios
            for li in tournament_list:
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
            
            if tournaments_by_date[date]:
                print(f"Migrados {len(tournaments_by_date[date])} torneios do formato antigo para {date}")
    
    return tournaments_by_date

def generate_html(new_tournaments):
    """Gera o novo conteúdo HTML com separador por dia e opção de download diário."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_datetime = today.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ler HTML existente e extrair torneios por data
    existing_html = read_existing_html()
    existing_tournaments_by_date = extract_existing_tournaments_by_date(existing_html)
    
    # Debug: mostrar quantos dias de histórico temos
    if existing_tournaments_by_date:
        total_existing = sum(len(tournaments) for tournaments in existing_tournaments_by_date.values())
        print(f"\n📚 Histórico existente: {len(existing_tournaments_by_date)} dias, {total_existing} torneios total")
        oldest_date = min(existing_tournaments_by_date.keys())
        newest_date = max(existing_tournaments_by_date.keys())
        print(f"   Período: {oldest_date} até {newest_date}")
    else:
        print("\n📚 Nenhum histórico existente encontrado")
    
    # Adicionar novos torneios ao dia de hoje
    if new_tournaments:
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
    else:
        print("\n⚠️ Nenhum torneio novo para adicionar hoje, mantendo histórico existente")
    
    # Remover datas antigas (mais de DAYS_TO_KEEP dias)
    cutoff_date = today - timedelta(days=DAYS_TO_KEEP)
    dates_to_remove = []
    for date_str in existing_tournaments_by_date.keys():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj < cutoff_date:
                dates_to_remove.append(date_str)
        except:
            # Se não conseguir processar a data, não remover
            print(f"⚠️ Não foi possível processar a data: {date_str}")
            continue
    
    if dates_to_remove:
        print(f"\n🗑️ Removendo {len(dates_to_remove)} datas antigas (mais de {DAYS_TO_KEEP} dias)")
        for date_str in dates_to_remove:
            del existing_tournaments_by_date[date_str]
            print(f"   Removida: {date_str}")
    else:
        print(f"\n✅ Nenhuma data antiga para remover (limite: {DAYS_TO_KEEP} dias)")
    
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
        <p>📅 Histórico mantido por até 365 dias</p>
    </footer>
</body>
</html>"""
    
    # Salvar o arquivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Resumo final
    total_tournaments = sum(len(tournaments) for tournaments in existing_tournaments_by_date.values())
    print(f"\n✅ Arquivo {OUTPUT_FILE} atualizado com sucesso!")
    print(f"📊 Resumo: {len(existing_tournaments_by_date)} dias de histórico, {total_tournaments} torneios total")

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
