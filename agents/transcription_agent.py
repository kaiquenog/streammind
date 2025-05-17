from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from utils.common import extract_video_id

def agente_transcritor(youtube_urls):
    """Agente que transcreve vídeos do YouTube"""
    print("Obtendo transcrições dos vídeos...")
    transcripts = []
    urls_processadas = 0
    
    for i, url in enumerate(youtube_urls, 1):
        if "Nenhum podcast relevante encontrado" in url:
            continue
            
        try:
            # Extrair o ID do vídeo da URL de forma mais robusta
            video_id = extract_video_id(url)
            
            if not video_id:
                print(f" - Erro: Não foi possível extrair o ID do vídeo de {url}")
                continue
                
            print(f" - Buscando transcrição para vídeo {i}: {url} (ID: {video_id})")
            
            # Obter a transcrição (tentando em várias línguas)
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
                print(f"   ✓ Transcrição encontrada em português")
            except:
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    print(f"   ✓ Transcrição encontrada em inglês")
                except:
                    try:
                        # Tentar sem especificar idioma
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                        print(f"   ✓ Transcrição encontrada (idioma não especificado)")
                    except Exception as e:
                        print(f"   ✗ Falha ao obter transcrição em qualquer idioma: {str(e)}")
                        continue
                
            # Montar o texto da transcrição
            transcript_text = " ".join([line['text'] for line in transcript_list])
            
            # Verificar se a transcrição tem conteúdo suficiente
            if len(transcript_text) < 100:
                print(f"   ✗ Transcrição muito curta ({len(transcript_text)} caracteres), ignorando")
                continue
                
            # Limitar o tamanho da transcrição para evitar problemas com modelos
            if len(transcript_text) > 20000:  # Limite prudente para o contexto do modelo
                print(f"   ⚠️ Transcrição muito longa ({len(transcript_text)} caracteres), truncando")
                transcript_text = transcript_text[:20000] + "... [transcrição truncada devido ao tamanho]"
                
            transcripts.append(f"### Transcrição do vídeo {i}: {url}\n\n{transcript_text}\n\n---\n")
            print(f" ✓ Transcrição completa obtida para {url} ({len(transcript_text)} caracteres)")
            urls_processadas += 1

        except NoTranscriptFound:
            print(f" - Aviso: Nenhuma transcrição encontrada para {url}.")
        except TranscriptsDisabled:
            print(f" - Aviso: Transcrições desabilitadas para {url}.")
        except Exception as e:
            print(f" - Erro ao obter transcrição para {url}: {str(e)}")

    if not transcripts:
        print("❌ Não foi possível obter nenhuma transcrição válida.")
        return "Nenhuma transcrição pôde ser obtida."
    
    print(f"✅ Obtidas {urls_processadas} transcrições de {len(youtube_urls)} URLs")
    return "\n".join(transcripts)
