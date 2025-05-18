import re
import os
import traceback
import subprocess
from datetime import datetime
from gtts import gTTS

# Verificar se ffmpeg está instalado (necessário para pydub)
def is_ffmpeg_installed():
    try:
        # Tenta executar ffmpeg para ver se está instalado
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except FileNotFoundError:
        return False

# Importar pydub apenas se ffmpeg estiver disponível
FFMPEG_AVAILABLE = is_ffmpeg_installed()
if FFMPEG_AVAILABLE:
    try:
        from pydub import AudioSegment
        PYDUB_AVAILABLE = True
        print("\nℹ️ DEBUG: pydub e ffmpeg disponíveis para processamento avançado de áudio")
    except ImportError:
        PYDUB_AVAILABLE = False
        print("\n⚠️ AVISO: pydub não está instalado. Usando funcionalidade básica de síntese de voz.")
else:
    PYDUB_AVAILABLE = False
    print("\n⚠️ AVISO: ffmpeg não está instalado. Usando funcionalidade básica de síntese de voz.")
    print("\nℹ️ Para instalar ffmpeg: sudo apt-get install ffmpeg (Ubuntu/Debian) ou brew install ffmpeg (macOS)")


def agente_sintetizador_voz(script_texto):
    """Agente que converte o script do podcast em áudio com formato de podcast"""
    print("\n🔊 PASSO 5: Gerando áudio do podcast...")
    print("Tentando gerar áudio a partir do script...")
    
    # Verificar se o script é válido
    if script_texto in ["Não foi possível gerar um script de podcast sem resumos válidos.", "Ocorreu um erro ao gerar o script do podcast.", "Não foi possível gerar um script de podcast adequado a partir dos resumos."]:
        print("\n❌ ERRO: Não há script válido para gerar o áudio.")
        return "Não foi possível gerar o áudio do podcast sem um script válido."
    
    # Verificar se o script tem conteúdo
    if not script_texto or len(script_texto.strip()) < 100:
        print("\n❌ ERRO: Script muito curto ou vazio.")
        return "Não foi possível gerar o áudio do podcast com um script tão curto."
    
    print("\nℹ️ DEBUG: Script válido detectado. Tamanho: {} caracteres".format(len(script_texto)))
    
    try:
        # Nome base do arquivo de saída
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo_final = f"podcast_audio_{timestamp}.mp3"
        print("\nℹ️ DEBUG: Nome do arquivo de saída definido: {}".format(nome_arquivo_final))
        
        # Extrair título do podcast do script (assumindo que está na primeira linha após # ou ## )
        linhas = script_texto.split('\n')
        titulo_podcast = "Podcast StreamMind"  # Título padrão
        for linha in linhas[:10]:  # Verificar apenas as primeiras linhas
            if linha.startswith('#') and not linha.startswith('##'):
                titulo_podcast = re.sub(r'#+ ', '', linha).strip()
                print(f"\nℹ️ DEBUG: Título do podcast detectado: {titulo_podcast}")
                break
        
        print(f"\nℹ️ DEBUG: Usando título: {titulo_podcast}")
        
        # Dividir o script em seções para processamento separado
        # Identificar seções por cabeçalhos markdown (##)
        secoes = []
        secao_atual = {"titulo": "Introdução", "conteudo": ""}
        
        print("\nℹ️ DEBUG: Iniciando divisão do script em seções...")
        for linha in linhas:
            if linha.startswith('##'):
                if secao_atual["conteudo"].strip():
                    secoes.append(secao_atual)
                    print(f"\nℹ️ DEBUG: Seção adicionada: {secao_atual['titulo']} ({len(secao_atual['conteudo'])} caracteres)")
                secao_atual = {"titulo": re.sub(r'#+ ', '', linha).strip(), "conteudo": ""}
            else:
                secao_atual["conteudo"] += linha + "\n"
        
        # Adicionar a última seção se tiver conteúdo
        if secao_atual["conteudo"].strip():
            secoes.append(secao_atual)
            print(f"\nℹ️ DEBUG: Última seção adicionada: {secao_atual['titulo']} ({len(secao_atual['conteudo'])} caracteres)")
        
        print(f"\nℹ️ DEBUG: Total de seções identificadas: {len(secoes)}")
        
        # Se não houver seções identificadas, tratar o texto inteiro como uma única seção
        if not secoes:
            print("\n⚠️ AVISO: Nenhuma seção identificada no script. Usando texto completo como uma única seção.")
            texto_limpo = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', script_texto)
            # Criar objeto gTTS básico
            tts = gTTS(text=texto_limpo, lang='pt', slow=False)
            tts.save(nome_arquivo_final)
            print(f"✅ Áudio básico do podcast gerado com sucesso: {nome_arquivo_final}")
            return nome_arquivo_final
        
        # Se pydub estiver disponível, criar um podcast com múltiplas vozes e transições
        if PYDUB_AVAILABLE:
            print("\nℹ️ DEBUG: Usando pydub para processamento avançado de áudio")
            try:
                # Criar diretório temporário para arquivos de áudio
                temp_dir = "temp_audio"
                print(f"\nℹ️ DEBUG: Criando diretório temporário: {temp_dir}")
                os.makedirs(temp_dir, exist_ok=True)
                
                # Inicializar áudio completo
                print("\nℹ️ DEBUG: Inicializando segmento de áudio vazio")
                audio_completo = AudioSegment.silent(duration=500)  # Começar com meio segundo de silêncio
                
                # Adicionar introdução
                print("\nℹ️ DEBUG: Gerando áudio de introdução")
                intro_text = f"Bem-vindo ao {titulo_podcast}. Um podcast gerado por IA que traz os principais insights sobre o tema de hoje."
                intro_file = os.path.join(temp_dir, f"intro_{timestamp}.mp3")
                print(f"\nℹ️ DEBUG: Salvando introdução em: {intro_file}")
                tts_intro = gTTS(text=intro_text, lang='pt', slow=False)
                tts_intro.save(intro_file)
                
                # Verificar se o arquivo foi criado
                if os.path.exists(intro_file):
                    print(f"\nℹ️ DEBUG: Arquivo de introdução criado com sucesso. Tamanho: {os.path.getsize(intro_file)} bytes")
                else:
                    print(f"\n❌ ERRO: Arquivo de introdução não foi criado!")
                
                # Adicionar a introdução ao áudio completo
                print("\nℹ️ DEBUG: Adicionando introdução ao áudio completo")
                audio_completo += AudioSegment.from_mp3(intro_file)
                audio_completo += AudioSegment.silent(duration=1000)  # 1 segundo de pausa
                print("\nℹ️ DEBUG: Introdução adicionada com sucesso")
            except Exception as e:
                print(f"\n❌ ERRO durante o processamento da introdução: {str(e)}")
                print("\n❌ Traceback completo:")
                traceback.print_exc()
            
            try:
                # Processar cada seção
                print(f"\nℹ️ DEBUG: Processando {len(secoes)} seções do podcast")
                for i, secao in enumerate(secoes):
                    print(f"\nℹ️ DEBUG: Processando seção {i+1}/{len(secoes)}: {secao['titulo']}")
                    # Limpar formatação markdown do conteúdo
                    texto_secao = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', secao["conteudo"])
                    print(f"\nℹ️ DEBUG: Texto da seção limpo, tamanho: {len(texto_secao)} caracteres")
                    
                    # Anúncio da seção
                    if i > 0:  # Não anunciar a primeira seção se for a introdução
                        print(f"\nℹ️ DEBUG: Gerando anúncio para a seção {secao['titulo']}")
                        anuncio_secao = f"Agora, vamos para a seção: {secao['titulo']}."
                        anuncio_file = os.path.join(temp_dir, f"anuncio_secao_{i}_{timestamp}.mp3")
                        tts_anuncio = gTTS(text=anuncio_secao, lang='pt', slow=False)
                        tts_anuncio.save(anuncio_file)
                        print(f"\nℹ️ DEBUG: Anúncio salvo em {anuncio_file}")
                        
                        audio_completo += AudioSegment.from_mp3(anuncio_file)
                        audio_completo += AudioSegment.silent(duration=700)  # Pausa curta
                        print("\nℹ️ DEBUG: Anúncio adicionado ao áudio completo")
                    
                    # Conteúdo da seção
                    print(f"\nℹ️ DEBUG: Gerando áudio para o conteúdo da seção {i+1}")
                    secao_file = os.path.join(temp_dir, f"secao_{i}_{timestamp}.mp3")
                    tts_secao = gTTS(text=texto_secao, lang='pt', slow=False)
                    tts_secao.save(secao_file)
                    print(f"\nℹ️ DEBUG: Áudio da seção salvo em {secao_file}")
                    
                    audio_completo += AudioSegment.from_mp3(secao_file)
                    audio_completo += AudioSegment.silent(duration=1000)  # Pausa entre seções
                    print("\nℹ️ DEBUG: Conteúdo da seção adicionado ao áudio completo")
                
                # Adicionar conclusão
                print("\nℹ️ DEBUG: Gerando áudio de conclusão")
                outro_text = f"Isso conclui nosso podcast de hoje sobre {titulo_podcast}. Obrigado por ouvir e até o próximo episódio!"
                outro_file = os.path.join(temp_dir, f"outro_{timestamp}.mp3")
                tts_outro = gTTS(text=outro_text, lang='pt', slow=False)
                tts_outro.save(outro_file)
                print(f"\nℹ️ DEBUG: Áudio de conclusão salvo em {outro_file}")
                
                audio_completo += AudioSegment.from_mp3(outro_file)
                print("\nℹ️ DEBUG: Conclusão adicionada ao áudio completo")
                
                # Exportar áudio final
                print(f"\nℹ️ DEBUG: Exportando áudio final para {nome_arquivo_final}")
                audio_completo.export(nome_arquivo_final, format="mp3")
                print(f"\nℹ️ DEBUG: Áudio final exportado com sucesso")
                
                # Limpar arquivos temporários
                print("\nℹ️ DEBUG: Limpando arquivos temporários")
                for arquivo in os.listdir(temp_dir):
                    try:
                        os.remove(os.path.join(temp_dir, arquivo))
                        print(f"\nℹ️ DEBUG: Arquivo temporário removido: {arquivo}")
                    except Exception as e:
                        print(f"\n⚠️ AVISO: Erro ao remover arquivo temporário {arquivo}: {e}")
                try:
                    os.rmdir(temp_dir)
                    print(f"\nℹ️ DEBUG: Diretório temporário {temp_dir} removido")
                except Exception as e:
                    print(f"\n⚠️ AVISO: Erro ao remover diretório temporário: {e}")
                
                duracao_segundos = len(audio_completo) / 1000.0
                print(f"✅ Podcast gerado com sucesso: {nome_arquivo_final}")
                print(f"   Duração: {int(duracao_segundos // 60)}m {int(duracao_segundos % 60)}s")
                return nome_arquivo_final
                
            except Exception as e:
                print(f"\n❌ ERRO durante o processamento das seções ou finalização: {str(e)}")
                print("\n❌ Traceback completo:")
                traceback.print_exc()
                # Tentar limpar arquivos temporários mesmo em caso de erro
                if 'temp_dir' in locals():
                    print("\nℹ️ Tentando limpar arquivos temporários após erro...")
                    try:
                        for arquivo in os.listdir(temp_dir):
                            try:
                                os.remove(os.path.join(temp_dir, arquivo))
                            except:
                                pass
                        try:
                            os.rmdir(temp_dir)
                        except:
                            pass
                    except:
                        pass
        else:
            # Versão simplificada sem pydub
            print("\nℹ️ DEBUG: pydub não disponível, usando método simplificado de geração de áudio")
            try:
                texto_completo = f"Bem-vindo ao {titulo_podcast}. \n\n"
                print("\nℹ️ DEBUG: Iniciando construção do texto completo para síntese")
                
                for i, secao in enumerate(secoes):
                    print(f"\nℹ️ DEBUG: Processando seção {i+1}/{len(secoes)}: {secao['titulo']}")
                    texto_limpo = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', secao["conteudo"])
                    texto_completo += f"Seção: {secao['titulo']}\n{texto_limpo}\n\n"
                    print(f"\nℹ️ DEBUG: Seção {secao['titulo']} adicionada ao texto completo")
                
                texto_completo += f"Isso conclui nosso podcast de hoje sobre {titulo_podcast}. Obrigado por ouvir!"
                print("\nℹ️ DEBUG: Conclusão adicionada ao texto completo")
                
                # Remover qualquer formatação markdown restante
                texto_final = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', texto_completo)
                print(f"\nℹ️ DEBUG: Texto final preparado para síntese, tamanho: {len(texto_final)} caracteres")
                
                # Verificar tamanho do texto (gTTS pode ter problemas com textos muito longos)
                if len(texto_final) > 100000:
                    print(f"\n⚠️ AVISO: Texto muito longo ({len(texto_final)} caracteres), pode causar problemas com gTTS")
                    # Truncar o texto se for muito longo
                    texto_final = texto_final[:99000] + "\n\nO texto foi truncado devido ao tamanho. Obrigado por ouvir!"
                    print("\nℹ️ DEBUG: Texto truncado para evitar problemas com gTTS")
                
                # Criar objeto gTTS
                print("\nℹ️ DEBUG: Criando objeto gTTS para síntese de voz")
                tts = gTTS(text=texto_final, lang='pt', slow=False)
                
                # Salvar o arquivo de áudio
                print(f"\nℹ️ DEBUG: Salvando áudio em {nome_arquivo_final}")
                tts.save(nome_arquivo_final)
                
                # Verificar se o arquivo foi criado
                if os.path.exists(nome_arquivo_final):
                    tamanho_arquivo = os.path.getsize(nome_arquivo_final)
                    print(f"\nℹ️ DEBUG: Arquivo de áudio criado com sucesso. Tamanho: {tamanho_arquivo} bytes")
                else:
                    print(f"\n❌ ERRO: Arquivo de áudio não foi criado!")
                
                print(f"✅ Áudio do podcast gerado com sucesso: {nome_arquivo_final}")
                return nome_arquivo_final
                
            except Exception as e:
                print(f"\n❌ ERRO durante a geração simplificada de áudio: {str(e)}")
                print("\n❌ Traceback completo:")
                traceback.print_exc()
                return f"Ocorreu um erro ao gerar o áudio do podcast: {str(e)}"

    
    except Exception as e:
        print(f"❌ Erro ao gerar o áudio do podcast: {str(e)}")
        print("❌ Traceback completo do erro:")
        traceback.print_exc()
        return f"Ocorreu um erro ao gerar o áudio do podcast: {str(e)}"
