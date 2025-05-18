import re
from datetime import datetime
from gtts import gTTS

def agente_sintetizador_voz(script_texto):
    """Agente que converte o script do podcast em áudio"""
    print("🔊 PASSO 5: Gerando áudio do podcast...")
    
    # Verificar se o script é válido
    if script_texto in ["Não foi possível gerar um script de podcast sem resumos válidos.", "Ocorreu um erro ao gerar o script do podcast.", "Não foi possível gerar um script de podcast adequado a partir dos resumos."]:
        print("❌ Não há script válido para gerar o áudio.")
        return "Não foi possível gerar o áudio do podcast sem um script válido."
    
    print("Tentando gerar áudio a partir do script...")
    
    try:
        
        print("⚠️ Funcionalidade de síntese de voz não implementada completamente")
        
        # Extrair apenas o texto sem formatação markdown para a síntese de voz
        texto_limpo = re.sub(r'#+ |\*\*|\*|`|_|\[|\]\(.*?\)', '', script_texto)
        
        # Criar objeto gTTS
        tts = gTTS(text=texto_limpo, lang='pt', slow=False)
        
        # Nome do arquivo de saída
        nome_arquivo = f"podcast_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        
        # Salvar o arquivo de áudio
        tts.save(nome_arquivo)
        
        print(f"✅ Áudio do podcast gerado com sucesso: {nome_arquivo}")
        return nome_arquivo
        
        return "Funcionalidade de síntese de voz em desenvolvimento. O script está pronto para ser narrado."
        
    except Exception as e:
        print(f"❌ Erro ao gerar o áudio do podcast: {str(e)}")
        return "Ocorreu um erro ao gerar o áudio do podcast."
