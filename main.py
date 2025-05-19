import warnings
import os
from dotenv import load_dotenv
from IPython.display import display

import typer
from pathlib import Path

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

app = typer.Typer(help="StreamMind CLI: Gere podcasts sobre tópicos de seu interesse usando múltiplos agentes de IA.")


@app.command("generate")
def main(
    topic: str = typer.Option(..., "-t", "--topic", help="Tópico para gerar o podcast, ex: 'IA e Agents de IA'"),
    max_videos: int = typer.Option(5, "-n", "--max-videos", help="Número máximo de vídeos a buscar (default: 5)"),
    output_dir: Path = typer.Option(Path("."), "-o", "--output-dir", help="Diretório para salvar scripts e áudio"),
    no_audio: bool = typer.Option(False, "--no-audio", help="Não gerar áudio do podcast"),
):
    """Gera um podcast em Markdown (e opcionalmente em MP3) para um determinado tópico."""
    typer.echo("🚀 Iniciando o Sistema de Geração de Podcast com Agentes 🚀")

    # Passo 1: Buscar podcasts no YouTube
    typer.echo(f"\n🔍 PASSO 1: Buscando até {max_videos} podcasts relevantes no YouTube sobre '{topic}'...")
    urls = agente_buscador_youtube(topic, data_de_hoje, max_videos)
    
    # Verificação de resultados
    if not urls or urls[0] == "Nenhum podcast relevante encontrado.":
        typer.secho("❌ Nenhum podcast relevante encontrado para o tópico informado.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"✅ Encontrados {len(urls)} podcasts potencialmente relevantes:", fg=typer.colors.GREEN)
    for i, url in enumerate(urls, 1):
        typer.echo(f"  {i}. {url}")
    
    # Passo 2: Obter transcrições
    typer.echo("\n🎯 PASSO 2: Obtendo transcrições dos podcasts...")
    transcripts = agente_transcritor(urls)
    if not transcripts or transcripts == "Nenhuma transcrição pôde ser obtida.":
        typer.secho("❌ Não foi possível obter transcrições para os podcasts encontrados.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Passo 3: Resumir as transcrições
    typer.echo("\n📝 PASSO 3: Resumindo as transcrições...")
    resumos = agente_resumidor(transcripts)

    # Passo 4: Gerar script do podcast
    typer.echo("\n🎙️ PASSO 4: Gerando script do podcast baseado nos resumos...")
    script_final = agente_sintetizador(resumos)
    typer.secho("\n🏆 PODCAST GERADO COM SUCESSO! 🏆", fg=typer.colors.GREEN)

    # Exibir e salvar o script em Markdown
    typer.echo("\nAqui está o script final do seu podcast:")
    display(to_markdown(script_final))
    output_dir.mkdir(parents=True, exist_ok=True)
    script_path = output_dir / f"podcast_script_{topic.replace(' ', '_')}.md"
    script_path.write_text(script_final, encoding="utf-8")
    typer.secho(f"Script salvo em: {script_path}", fg=typer.colors.BLUE)

    # Passo 5: Gerar áudio do podcast (opcional)
    if not no_audio:
        typer.echo("\n🔊 PASSO 5: Gerando áudio do podcast...")
        audio_resultado = agente_sintetizador_voz(script_final)
        typer.secho(f"Áudio gerado: {audio_resultado}", fg=typer.colors.BLUE)
    else:
        typer.secho("🔊 Geração de áudio ignorada (--no-audio)", fg=typer.colors.YELLOW)


def _version_callback(value: bool):
    if value:
        typer.echo("StreamMind CLI Version: 1.0.0")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", callback=_version_callback, is_eager=True, help="Exibe a versão do CLI."),
):
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'generate' para criar um podcast. Veja --help para mais opções.")

if __name__ == "__main__":
    app()
