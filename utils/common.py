import textwrap
import re
from IPython.display import Markdown
from datetime import date

# Função auxiliar para exibir texto formatado em Markdown no Colab
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def extract_video_id(url):
    """Extrair o ID do vídeo da URL do YouTube de forma mais robusta"""
    # Padrão para URL completa (watch?v=XXXXXXXXXXX)
    if "youtube.com/watch?v=" in url:
        try:
            video_id = url.split("v=")[1]
            # Remover parâmetros adicionais após o ID
            ampersand_pos = video_id.find('&')
            if ampersand_pos != -1:
                video_id = video_id[:ampersand_pos]
            return video_id if len(video_id) == 11 else None
        except:
            return None
    
    # Padrão para URL encurtada (youtu.be/XXXXXXXXXXX)
    elif "youtu.be/" in url:
        try:
            video_id = url.split("youtu.be/")[1]
            # Remover parâmetros adicionais após o ID
            slash_pos = video_id.find('/')
            if slash_pos != -1:
                video_id = video_id[:slash_pos]
            question_pos = video_id.find('?')
            if question_pos != -1:
                video_id = video_id[:question_pos]
            return video_id if len(video_id) == 11 else None
        except:
            return None
            
    # Usar regex como backup
    else:
        youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(youtube_regex, url)
        if match:
            return match.group(1)
    
    return None

# Obter a data atual formatada
def get_current_date():
    return date.today().strftime("%d/%m/%Y")
