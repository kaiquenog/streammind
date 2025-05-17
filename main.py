import warnings
import os
from dotenv import load_dotenv
from IPython.display import display

# Import utility modules
from utils.common import to_markdown, get_current_date

# Import agent modules
from agents.youtube_search_agent import agente_buscador_youtube
from agents.transcription_agent import agente_transcritor
from agents.summary_agent import agente_resumidor
from agents.synthesis_agent import agente_sintetizador
from agents.speech_synthesis_agent import agente_sintetizador_voz

# Load environment variables and configure settings
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
warnings.filterwarnings("ignore")

# Get current date
data_de_hoje = get_current_date()

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
    
    # Verificação melhorada
    if not urls:
        print("❌ Não foram encontradas URLs de podcasts.")
        return
    
    if urls[0] == "Nenhum podcast relevante encontrado.":
        print("❌ Não foi possível encontrar podcasts relevantes sobre este tópico.")
        return
    
    print(f"✅ Encontrados {len(urls)} podcasts potencialmente relevantes:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    # Passo 2: Obter transcrições
    print("\n🎯 PASSO 2: Obtendo transcrições dos podcasts...")
    transcripts = agente_transcritor(urls)
    
    if not transcripts or transcripts == "Nenhuma transcrição pôde ser obtida.":
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
    
    # Passo 5: Gerar áudio do podcast (opcional)
    print("\n🔊 PASSO 5 (OPCIONAL): Gerando áudio do podcast...")
    audio_resultado = agente_sintetizador_voz(script_final)
    print(f"\nResultado da síntese de voz: {audio_resultado}")


if __name__ == "__main__":
    main()
