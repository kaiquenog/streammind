from google.adk.agents import Agent
from utils.agent_communication import call_agent
from datetime import date

def agente_sintetizador(resumos_texto):
    """Agente que sintetiza os resumos em um script de podcast"""
    if resumos_texto in ["Não foi possível gerar resumos sem transcrições.", "Nenhuma transcrição pôde ser obtida.", "Ocorreu um erro ao gerar os resumos das transcrições.", "Não foi possível gerar resumos adequados das transcrições."]:
        print("❌ Não há resumos válidos para gerar o script do podcast.")
        return "Não foi possível gerar um script de podcast sem resumos válidos."

    print("Sintetizando o script final do podcast...")
    
    # Verificar o tamanho dos resumos para evitar exceder o contexto do modelo
    if len(resumos_texto) > 30000:
        print(f"⚠️ Resumos muito longos ({len(resumos_texto)} caracteres), truncando para evitar exceder o contexto do modelo")
        # Truncar de forma inteligente, mantendo a estrutura
        resumos_texto = resumos_texto[:30000] + "\n\n[Conteúdo adicional foi truncado devido ao tamanho]"
        print(f"Resumos truncados para {len(resumos_texto)} caracteres")
    
    sintetizador = Agent(
        name="agente_sintetizador",
        model="gemini-2.5-pro-preview-03-25",
        instruction="""
        Você é um roteirista profissional de podcasts especializados em Inteligência Artificial e Agentes de IA.
        
        Sua tarefa é criar um script completo para um episódio de podcast baseado nos resumos fornecidos.
        O podcast deve ser informativo, envolvente e acessível tanto para iniciantes quanto para pessoas com conhecimento em IA.
        
        Estruture o script da seguinte forma:
        
        1. TÍTULO E INTRODUÇÃO:
           - Crie um título cativante e relevante para o episódio
           - Faça uma abertura que desperte interesse imediato no tema de IA e Agentes
           - Contextualize a importância atual da IA e dos agentes inteligentes
           - Apresente brevemente os principais tópicos que serão abordados
        
        2. DESENVOLVIMENTO (divida em segmentos claros):
           - Organize o conteúdo em 3-5 segmentos temáticos baseados nos resumos
           - Para cada segmento:
              * Apresente os conceitos-chave de forma clara e acessível
              * Explique aplicações práticas e exemplos do mundo real
              * Discuta implicações e impactos futuros
           - Inclua transições naturais entre os segmentos
           - Incorpore citações relevantes dos especialistas mencionados nos resumos
        
        3. DISCUSSÃO DE TENDÊNCIAS E FUTURO:
           - Analise as tendências emergentes em IA e Agentes mencionadas nos resumos
           - Discuta desafios, limitações e considerações éticas
           - Explore possíveis desenvolvimentos futuros
        
        4. CONCLUSÃO E CHAMADA PARA AÇÃO:
           - Sintetize os principais insights e aprendizados
           - Ofereça uma reflexão final sobre o impacto da IA e dos agentes
           - Sugira recursos adicionais para os ouvintes que queiram se aprofundar
           - Convide os ouvintes a continuarem a conversa e compartilharem suas opiniões
        
        ORIENTAÇÕES DE ESTILO E TOM:
        - Use linguagem conversacional, como se estivesse falando diretamente com o ouvinte
        - Alterne entre explicações técnicas simplificadas e insights mais profundos
        - Inclua momentos de curiosidade e surpresa para manter o engajamento
        - Faça perguntas retóricas ocasionais para estimular a reflexão
        - Mantenha um equilíbrio entre otimismo sobre o potencial da IA e uma visão crítica dos desafios
        - O script deve ter entre 1500-2500 palavras e ser estruturado em parágrafos claros
        
        IMPORTANTE: Marque claramente as seções principais do podcast com títulos em negrito.
        """,
        description="Agente que sintetiza resumos em um script de podcast profissional sobre IA e Agentes.",
    )

    try:
        print(f"Enviando {len(resumos_texto)} caracteres para o agente sintetizador...")
        entrada_do_agente = f"Aqui estão os resumos dos podcasts sobre IA e Agentes de IA para criar um script profissional:\n\n{resumos_texto}"
        script_do_podcast = call_agent(sintetizador, entrada_do_agente)
        
        if not script_do_podcast or len(script_do_podcast.strip()) < 500:
            print("⚠️ O agente sintetizador retornou um script muito curto ou vazio")
            return "Não foi possível gerar um script de podcast adequado a partir dos resumos."
        
        # Adicionar metadados ao script
        data_atual = date.today().strftime("%d/%m/%Y")
        script_final = f"# StreamMind Podcast - Episódio Gerado por IA\n\n*Data de geração: {data_atual}*\n\n---\n\n{script_do_podcast}\n\n---\n\n*Este script foi gerado automaticamente pelo sistema StreamMind utilizando agentes de IA.*"
        
        print(f"✅ Script do podcast gerado com sucesso ({len(script_final)} caracteres)")
        return script_final
    except Exception as e:
        print(f"❌ Erro ao gerar o script do podcast: {str(e)}")
        return "Ocorreu um erro ao gerar o script do podcast."
