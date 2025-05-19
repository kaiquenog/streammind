from google.adk.agents import Agent
from google.adk.tools import google_search
from utils.agent_communication import call_agent
from utils.common import extract_video_id

def agente_buscador_youtube(topico, data_de_hoje, max_results=5):
    """Agente que busca podcasts no YouTube sobre um tópico específico"""
    print("Buscando podcasts no YouTube...")
    
    # Tentar diferentes consultas de busca para maximizar as chances de encontrar resultados
    consultas = [
        f"{topico}",
        f"podcasts YouTube {topico} 2025",
        f"entrevista YouTube {topico} recente",
        f"vídeo podcast {topico} YouTube",
        f"{topico} podcast episódio completo YouTube",
        f"YouTube {topico} conversa especialistas"
    ]
    
    todas_urls = []
    
    for i, consulta in enumerate(consultas, 1):
        print(f"Tentativa {i}: Buscando com a consulta: '{consulta}'...")
        
        buscador = Agent(
            name="agente_buscador_youtube",
            model="gemini-2.0-flash",
            instruction=f"""
                         Você é um assistente de busca especializado em encontrar vídeos no YouTube.
                         
                         Sua tarefa é encontrar URLs de vídeos no YouTube relacionados a "{topico}".
                         
                         SIGA ESTES PASSOS:
                         1. Use a ferramenta `google_search` com a consulta que vou te fornecer.
                         2. Analise os resultados e identifique URLs do YouTube (começando com https://www.youtube.com/ ou https://youtu.be/).
                         3. Retorne APENAS as URLs do YouTube encontradas, uma por linha, sem numeração ou texto adicional.
                         
                         IMPORTANTE:
                         - NÃO invente URLs.
                         - NÃO adicione comentários ou explicações.
                         - Se não encontrar nenhuma URL do YouTube, responda apenas: "Nenhum resultado encontrado."
                         """,
            description="Agente que busca videos no YouTube usando a busca do Google.",
            tools=[google_search]
        )

        entrada_do_agente = f"Busca: {consulta}"
        resultado = call_agent(buscador, entrada_do_agente)
        
        print(f"RESULTADO DA BUSCA {i}:\n{resultado}\n")
        
        # Processar o resultado para extrair URLs do YouTube
        urls_desta_busca = []
        for linha in resultado.strip().split('\n'):
            linha = linha.strip()
            linha = linha.replace('*', '').strip()  # Remover marcadores
            
            # Verificar se a linha contém uma URL do YouTube
            if "youtube.com" in linha or "youtu.be" in linha:
                # Extrair a URL do YouTube da linha (pode conter texto adicional)
                youtube_url = None
                if "youtube.com/watch?v=" in linha:
                    start_idx = linha.find("https://www.youtube.com/watch?v=")
                    if start_idx == -1:  # Tentar sem https://
                        start_idx = linha.find("www.youtube.com/watch?v=")
                        if start_idx != -1:
                            youtube_url = "https://" + linha[start_idx:].split()[0].strip()
                    else:
                        youtube_url = linha[start_idx:].split()[0].strip()
                elif "youtu.be/" in linha:
                    start_idx = linha.find("https://youtu.be/")
                    if start_idx == -1:  # Tentar sem https://
                        start_idx = linha.find("youtu.be/")
                        if start_idx != -1:
                            youtube_url = "https://" + linha[start_idx:].split()[0].strip()
                    else:
                        youtube_url = linha[start_idx:].split()[0].strip()
                
                if youtube_url:
                    # Limpar a URL (remover parâmetros desnecessários)
                    if '&' in youtube_url:
                        youtube_url = youtube_url.split('&')[0]
                    
                    # Verificar se o ID do vídeo parece válido
                    video_id = extract_video_id(youtube_url)
                    if video_id:
                        urls_desta_busca.append(youtube_url)
        
        # Adicionar URLs únicas desta busca ao conjunto total
        for url in urls_desta_busca:
            if url not in todas_urls:
                todas_urls.append(url)
        
        print(f"URLs encontradas nesta busca: {len(urls_desta_busca)}")
        
        # Se já temos URLs suficientes, podemos parar
        if len(todas_urls) >= max_results:
            break
    
    # Verificar se encontramos URLs válidas
    if not todas_urls:
        print("❌ Nenhuma URL válida do YouTube encontrada após todas as tentativas.")
        return ["Nenhum podcast relevante encontrado."]
    
    # Imprimir para depuração
    print(f"✅ Total de URLs válidas encontradas: {len(todas_urls)}")
    for i, url in enumerate(todas_urls, 1):
        print(f" {i}. {url}")
    
    return todas_urls[:max_results]
