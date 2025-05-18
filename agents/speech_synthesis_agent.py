import re
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment


def agente_sintetizador_voz(script_texto):
    """Agente que converte o script do podcast em áudio com formato de podcast"""
    print("\n🔊 PASSO 5: Gerando áudio do podcast...")
    print("Tentando gerar áudio a partir do script...")
    
    try:
        # Nome base do arquivo de saída
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo_final = f"podcast_audio_{timestamp}.mp3"
        
        # Extrair título do podcast do script (assumindo que está na primeira linha após # ou ## )
        linhas = script_texto.split('\n')
        titulo_podcast = "Podcast StreamMind"  # Título padrão
        for linha in linhas[:10]:  # Verificar apenas as primeiras linhas
            if linha.startswith('#') and not linha.startswith('##'):
                titulo_podcast = re.sub(r'#+ ', '', linha).strip()
                break
        
        # Dividir o script em seções para processamento separado
        # Identificar seções por cabeçalhos markdown (##)
        secoes = []
        secao_atual = {"titulo": "Introdução", "conteudo": ""}
        
        for linha in linhas:
            if linha.startswith('##'):
                if secao_atual["conteudo"].strip():
                    secoes.append(secao_atual)
                secao_atual = {"titulo": re.sub(r'#+ ', '', linha).strip(), "conteudo": ""}
            else:
                secao_atual["conteudo"] += linha + "\n"
        
        # Adicionar a última seção se tiver conteúdo
        if secao_atual["conteudo"].strip():
            secoes.append(secao_atual)
        
        # Se não houver seções identificadas, tratar o texto inteiro como uma única seção
        if not secoes:
            texto_limpo = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', script_texto)
            # Criar objeto gTTS básico
            tts = gTTS(text=texto_limpo, lang='pt', slow=False)
            tts.save(nome_arquivo_final)
            print(f"✅ Áudio básico do podcast gerado com sucesso: {nome_arquivo_final}")
            return nome_arquivo_final
        
        # Se pydub estiver disponível, criar um podcast com múltiplas vozes e transições
        if PYDUB_AVAILABLE:
            # Criar diretório temporário para arquivos de áudio
            temp_dir = "temp_audio"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Inicializar áudio completo
            audio_completo = AudioSegment.silent(duration=500)  # Começar com meio segundo de silêncio
            
            # Adicionar introdução
            intro_text = f"Bem-vindo ao {titulo_podcast}. Um podcast gerado por IA que traz os principais insights sobre o tema de hoje."
            intro_file = os.path.join(temp_dir, f"intro_{timestamp}.mp3")
            tts_intro = gTTS(text=intro_text, lang='pt', slow=False)
            tts_intro.save(intro_file)
            
            # Adicionar a introdução ao áudio completo
            audio_completo += AudioSegment.from_mp3(intro_file)
            audio_completo += AudioSegment.silent(duration=1000)  # 1 segundo de pausa
            
            # Processar cada seção
            for i, secao in enumerate(secoes):
                # Limpar formatação markdown do conteúdo
                texto_secao = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', secao["conteudo"])
                
                # Anúncio da seção
                if i > 0:  # Não anunciar a primeira seção se for a introdução
                    anuncio_secao = f"Agora, vamos para a seção: {secao['titulo']}."
                    anuncio_file = os.path.join(temp_dir, f"anuncio_secao_{i}_{timestamp}.mp3")
                    tts_anuncio = gTTS(text=anuncio_secao, lang='pt', slow=False)
                    tts_anuncio.save(anuncio_file)
                    
                    audio_completo += AudioSegment.from_mp3(anuncio_file)
                    audio_completo += AudioSegment.silent(duration=700)  # Pausa curta
                
                # Conteúdo da seção
                secao_file = os.path.join(temp_dir, f"secao_{i}_{timestamp}.mp3")
                tts_secao = gTTS(text=texto_secao, lang='pt', slow=False)
                tts_secao.save(secao_file)
                
                audio_completo += AudioSegment.from_mp3(secao_file)
                audio_completo += AudioSegment.silent(duration=1000)  # Pausa entre seções
            
            # Adicionar conclusão
            outro_text = f"Isso conclui nosso podcast de hoje sobre {titulo_podcast}. Obrigado por ouvir e até o próximo episódio!"
            outro_file = os.path.join(temp_dir, f"outro_{timestamp}.mp3")
            tts_outro = gTTS(text=outro_text, lang='pt', slow=False)
            tts_outro.save(outro_file)
            
            audio_completo += AudioSegment.from_mp3(outro_file)
            
            # Exportar áudio final
            audio_completo.export(nome_arquivo_final, format="mp3")
            
            # Limpar arquivos temporários
            for arquivo in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, arquivo))
                except Exception as e:
                    print(f"Erro ao remover arquivo temporário: {e}")
            try:
                os.rmdir(temp_dir)
            except Exception as e:
                print(f"Erro ao remover diretório temporário: {e}")
            
            duracao_segundos = len(audio_completo) / 1000.0
            print(f"✅ Podcast gerado com sucesso: {nome_arquivo_final}")
            print(f"   Duração: {int(duracao_segundos // 60)}m {int(duracao_segundos % 60)}s")
            return nome_arquivo_final
        else:
            # Versão simplificada sem pydub
            texto_completo = f"Bem-vindo ao {titulo_podcast}. \n\n"
            
            for secao in secoes:
                texto_limpo = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', secao["conteudo"])
                texto_completo += f"Seção: {secao['titulo']}\n{texto_limpo}\n\n"
            
            texto_completo += f"Isso conclui nosso podcast de hoje sobre {titulo_podcast}. Obrigado por ouvir!"
            
            # Remover qualquer formatação markdown restante
            texto_final = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', texto_completo)
            
            # Criar objeto gTTS
            tts = gTTS(text=texto_final, lang='pt', slow=False)
            
            # Salvar o arquivo de áudio
            tts.save(nome_arquivo_final)
            
            print(f"✅ Áudio do podcast gerado com sucesso: {nome_arquivo_final}")
            return nome_arquivo_final
    
    except Exception as e:
        print(f"❌ Erro ao gerar o áudio do podcast: {str(e)}")
        return "Ocorreu um erro ao gerar o áudio do podcast."
