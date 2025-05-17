from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
from IPython.display import display, Markdown # Para exibir texto formatado no Colab
import requests # Para fazer requisições HTTP
import warnings
from dotenv import load_dotenv
import os
import re
# Instalar a biblioteca youtube-transcript-api: pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

warnings.filterwarnings("ignore")

data_de_hoje = date.today().strftime("%d/%m/%Y")

def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    print(f"\nDEBUG: Enviando para o agente '{agent.name}': '{message_text}'")
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        # Tenta imprimir o tipo de evento se o atributo event_type existir
        if hasattr(event, 'event_type'):
            print(f"DEBUG: Evento recebido: Tipo='{event.event_type}'")
        else:
            # Se event_type não existir, imprime os atributos disponíveis para ajudar na depuração
            print(f"DEBUG: Evento recebido (atributos: {dir(event)})")

        if event.content and event.content.parts:
            for i, part in enumerate(event.content.parts):
                print(f"DEBUG: Evento Part[{i}]:")
                if part.text is not None:
                    print(f"  DEBUG: Part.text: '{part.text}'")

                # Logging para chamadas de função (comum com Gemini e google-adk)
                if hasattr(part, 'function_call') and part.function_call:
                    print(f"  DEBUG: Part.function_call: Name='{part.function_call.name}', Args='{part.function_call.args}'")

                # Logging para respostas de função/ferramenta
                if hasattr(part, 'function_response') and part.function_response:
                    print(f"  DEBUG: Part.function_response: Name='{part.function_response.name}', Response='{part.function_response.response}'")

                # Logging mais genérico para tool_code e tool_response, caso function_call não seja o único
                if hasattr(part, 'tool_code') and part.tool_code and not (hasattr(part, 'function_call') and part.function_call) : # Evitar duplicidade se function_call já foi logado
                    print(f"  DEBUG: Part.tool_code: Name='{part.tool_code.name}', Args='{part.tool_code.args}'")
                if hasattr(part, 'tool_response') and part.tool_response and not (hasattr(part, 'function_response') and part.function_response): # Evitar duplicidade
                    print(f"  DEBUG: Part.tool_response: Name='{part.tool_response.name}', Content='{part.tool_response.content}'")


        if event.is_final_response():
          print("DEBUG: Evento é resposta final.")
          if event.content and event.content.parts:
              for part in event.content.parts:
                if part.text is not None:
                  final_response += part.text
                  final_response += "\n"
    print(f"DEBUG: Resposta final bruta do agente '{agent.name}':\n{final_response.strip()}")
    return final_response.strip()

# Função auxiliar para exibir texto formatado em Markdown no Colab
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def extract_video_id(url):
    """Extrair o ID do vídeo da URL do YouTube de forma mais robusta"""
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, url)
    if match:
        return match.group(1)
    return None

def main():
    print("🚀 Iniciando o Sistema de Geração de Podcast com Agentes 🚀")
    
    topico = input("❓ Por favor, digite o TÓPICO sobre o qual você quer gerar o podcast (ex: IA e Agents de IA): ")

    if not topico:
        print("Você esqueceu de digitar o tópico!")
        return
    else:
        print(f"Maravilha! Vamos então buscar podcasts sobre {topico}")
    
    # Passo 1: Buscar podcasts no YouTube
    print("\n🔍 PASSO 1: Buscando podcasts relevantes no YouTube...")
    urls = agente_buscador_youtube(topico, data_de_hoje)
    
    if not urls or urls[0] == "Nenhum podcast relevante encontrado.":
        print("❌ Não foi possível encontrar podcasts relevantes sobre este tópico.")
        return
    
    print(f"✅ Encontrados {len(urls)} podcasts potencialmente relevantes:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    # Passo 2: Obter transcrições
    print("\n🎯 PASSO 2: Obtendo transcrições dos podcasts...")
    transcripts = agente_transcritor(urls)
    
    if transcripts == "Nenhuma transcrição pôde ser obtida.":
        print("❌ Não foi possível obter transcrições para nenhum dos podcasts encontrados.")
        return
    
    # Passo 3: Resumir as transcrições
    print("\n📝 PASSO 3: Resumindo as transcrições...")
    resumos = agente_resumidor(transcripts)
    
    # Passo 4: Gerar script do podcast
    print("\n🎙️ PASSO 4: Gerando script do podcast baseado nos resumos...")
    script_final = agente_sintetizador(resumos)
    
    # Exibir o resultado final
    print("\n🏆 PODCAST GERADO COM SUCESSO! 🏆")
    print("\nAqui está o script final do seu podcast:")
    display(to_markdown(script_final))
    
    # Opcionalmente, salvar o script em um arquivo
    with open(f"podcast_script_{topico.replace(' ', '_')}.md", "w", encoding="utf-8") as f:
        f.write(script_final)
    print(f"\nO script também foi salvo no arquivo 'podcast_script_{topico.replace(' ', '_')}.md'")


####################################################
# --- Agente 1: Buscador de Podcasts no YouTube --- #
####################################################
def agente_buscador_youtube(topico, data_de_hoje):
    print("Buscando podcasts no YouTube...")
    
    buscador = Agent(
        name="agente_buscador_youtube",
        model="gemini-1.5-flash-latest",
        instruction=f"""
                     Você é um assistente de busca especializado. Sua ÚNICA tarefa é encontrar URLs de vídeos de podcast no YouTube sobre "{topico}" que sejam recentes (publicados nos últimos 3 meses a partir de {data_de_hoje}).
                     
                     PARA FAZER ISSO, VOCÊ DEVE OBRIGATORIAMENTE SEGUIR ESTES PASSOS:
                     1.  **PRIMEIRO PASSO OBRIGATÓRIO:** Use a ferramenta `google_search`. Formule uma consulta de busca eficaz para encontrar "vídeos de podcast no YouTube sobre {topico} recentes".
                     2.  **SEGUNDO PASSO:** Analise CUIDADOSAMENTE os resultados retornados PELA FERRAMENTA `google_search`.
                     3.  **TERCEIRO PASSO:** Com base APENAS nos resultados da ferramenta, liste até 5 URLs COMPLETAS do YouTube (começando com https://www.youtube.com/ ou https://youtu.be/) que sejam realmente podcasts relevantes e recentes.
                     4.  **FORMATAÇÃO DA RESPOSTA:**
                         *   Se a ferramenta `google_search` retornar URLs relevantes que atendam aos critérios, liste CADA URL em uma NOVA LINHA, sem numeração, marcadores, ou qualquer outro texto introdutório ou conclusivo. APENAS AS URLs.
                         *   Se a ferramenta `google_search` não encontrar resultados relevantes ou se os resultados não forem podcasts dentro do período de 3 meses, responda EXATAMENTE com a frase: "Nenhum podcast relevante encontrado." Não adicione mais nada.
                     
                     NÃO invente URLs. NÃO forneça resumos ou descrições. Sua resposta deve ser APENAS a lista de URLs ou a frase "Nenhum podcast relevante encontrado.".
                     """,
        description="Agente que busca videoss sobre um tópico no YouTube usando a busca do Google.",
        tools=[google_search]
    )

    # O google_search será executado dentro do call_agent com base nas instruções do agente
    entrada_do_agente = f"Busque por podcasts no YouTube sobre: {topico}"
    resultado = call_agent(buscador, entrada_do_agente)
    
    # Processar o resultado para obter apenas URLs válidas do YouTube
    urls_encontradas = []
    for linha in resultado.strip().split('\n'):
        linha = linha.strip()
        if linha.startswith('https://www.youtube.com/') or linha.startswith('https://youtu.be/'):
            urls_encontradas.append(linha)
        elif "Nenhum podcast relevante encontrado" in linha:
            return ["Nenhum podcast relevante encontrado."]
    
    if not urls_encontradas:
        return ["Nenhum podcast relevante encontrado."]
    
    return urls_encontradas[:5]  # Limitando a 5 URLs no máximo

###########################################
# --- Agente 2: Transcritor de Vídeos --- #
###########################################
def agente_transcritor(youtube_urls):
    print("Obtendo transcrições dos vídeos...")
    transcripts = []
    
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
            
            # Obter a transcrição (tentando primeiro em português, depois em inglês)
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
            except:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                
            # Montar o texto da transcrição
            transcript_text = " ".join([line['text'] for line in transcript_list])
            
            # Limitar o tamanho da transcrição para evitar problemas com modelos
            if len(transcript_text) > 20000:  # Limite prudente para o contexto do modelo
                transcript_text = transcript_text[:20000] + "... [transcrição truncada devido ao tamanho]"
                
            transcripts.append(f"### Transcrição do vídeo {i}: {url}\n\n{transcript_text}\n\n---\n")
            print(f" ✓ Transcrição obtida para {url}")

        except NoTranscriptFound:
            print(f" - Aviso: Nenhuma transcrição encontrada para {url}.")
        except TranscriptsDisabled:
            print(f" - Aviso: Transcrições desabilitadas para {url}.")
        except Exception as e:
            print(f" - Erro ao obter transcrição para {url}: {str(e)}")

    if not transcripts:
        return "Nenhuma transcrição pôde ser obtida."
        
    return "\n".join(transcripts)


###########################################
# --- Agente 3: Resumidor de Textos --- #
###########################################
def agente_resumidor(transcripts_text):
    if transcripts_text == "Nenhuma transcrição pôde ser obtida.":
        return "Não foi possível gerar resumos sem transcrições."

    print("Resumindo as transcrições...")
    
    resumidor = Agent(
        name="agente_resumidor",
        model="gemini-2.5-pro-preview-03-25",
        instruction="""
        Você é um especialista em resumir conteúdo de podcasts e extrair os pontos-chave.
        
        Sua tarefa é ler as transcrições de podcasts fornecidas e criar um resumo estruturado e informativo.
        
        Para cada transcrição (separadas por "---"):
        1. Identifique o tópico principal do podcast
        2. Extraia os 5-8 pontos mais relevantes discutidos
        3. Inclua quaisquer insights únicos ou exemplos importantes mencionados
        4. Destaque citações impactantes se houver
        
        Formate seu resumo de forma organizada com:
        - Título para cada podcast resumido
        - Lista de pontos-chave com marcadores
        - Seção de conclusões ou insights principais
        
        Mantenha o resumo conciso e informativo, focando na qualidade das informações extraídas.
        """,
        description="Agente que resume transcrições de podcasts de forma estruturada",
    )

    entrada_do_agente = f"Aqui estão as transcrições para resumir:\n\n{transcripts_text}"
    resumos = call_agent(resumidor, entrada_do_agente)
    return resumos

##################################################
# --- Agente 4: Sintetizador de Podcast --- #
##################################################
def agente_sintetizador(resumos_texto):
    if resumos_texto in ["Não foi possível gerar resumos sem transcrições.", "Nenhuma transcrição pôde ser obtida."]:
         return "Não foi possível gerar um script de podcast sem resumos."

    print("Sintetizando o script final do podcast...")
    
    sintetizador = Agent(
        name="agente_sintetizador",
        model="gemini-2.5-pro-preview-03-25",
        instruction="""
        Você é um roteirista profissional de podcasts sobre tecnologia e IA.
        
        Sua tarefa é criar um script completo para um episódio de podcast baseado nos resumos fornecidos.
        O podcast deve ter um formato profissional e ser envolvente para o ouvinte.
        
        Estruture o script da seguinte forma:
        
        1. INTRODUÇÃO:
           - Uma abertura cativante que introduz o tema principal
           - Contextualização do assunto e sua relevância atual
           - Menção aos principais tópicos que serão abordados
        
        2. DESENVOLVIMENTO:
           - Divida o conteúdo em segmentos lógicos baseados nos principais pontos dos resumos
           - Para cada segmento, aprofunde-se nos conceitos mais interessantes 
           - Inclua transições suaves entre os segmentos
           - Use comparações, exemplos e metáforas para facilitar o entendimento
        
        3. CONCLUSÃO:
           - Sintetize os principais insights discutidos
           - Ofereça reflexões sobre o futuro do tema
           - Convide os ouvintes a refletirem ou explorarem mais sobre o assunto
        
        ORIENTAÇÕES IMPORTANTES:
        - Use um tom conversacional e acessível, como se estivesse realmente falando com ouvintes
        - Alterne entre momentos informativos e momentos mais descontraídos
        - Inclua perguntas retóricas ocasionais para manter o engajamento
        - Crie um título criativo e atraente para o episódio
        - O script deve ter entre 1500-2500 palavras
        - Marque claramente as seções do podcast (INTRODUÇÃO, DESENVOLVIMENTO, CONCLUSÃO)
        """,
        description="Agente que sintetiza resumos em um script de podcast profissional.",
    )

    entrada_do_agente = f"Aqui estão os resumos dos podcasts para criar um script:\n\n{resumos_texto}"
    script_do_podcast = call_agent(sintetizador, entrada_do_agente)
    return script_do_podcast


if __name__ == "__main__":
    main()