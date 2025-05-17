from google.adk.agents import Agent
from utils.agent_communication import call_agent

def agente_resumidor(transcripts_text):
    """Agente que resume as transcrições dos podcasts"""
    if transcripts_text == "Nenhuma transcrição pôde ser obtida.":
        print("❌ Não há transcrições para resumir.")
        return "Não foi possível gerar resumos sem transcrições."

    print("Resumindo as transcrições...")
    
    # Verificar o tamanho das transcrições para evitar exceder o contexto do modelo
    if len(transcripts_text) > 50000:
        print(f"⚠️ Transcrições muito longas ({len(transcripts_text)} caracteres), truncando para evitar exceder o contexto do modelo")
        # Dividir por marcadores de separação para preservar a estrutura
        partes = transcripts_text.split("---")
        # Manter apenas as primeiras partes até um limite razoável
        transcripts_text = "---".join(partes[:3]) + "\n\n[Conteúdo adicional foi truncado devido ao tamanho]"
        print(f"Transcrições truncadas para {len(transcripts_text)} caracteres")
    
    resumidor = Agent(
        name="agente_resumidor",
        model="gemini-2.5-pro-preview-03-25",
        instruction="""
        Você é um especialista em resumir conteúdo de podcasts e extrair os pontos-chave relacionados a Inteligência Artificial e Agentes de IA.
        
        Sua tarefa é ler as transcrições de podcasts fornecidas e criar um resumo estruturado e informativo, focando especificamente em conteúdo relacionado a IA e Agentes de IA.
        
        Para cada transcrição (separadas por "---"):
        1. Identifique o tópico principal do podcast e sua relação com IA/Agentes de IA
        2. Extraia os 5-8 pontos mais relevantes discutidos sobre IA, dando prioridade a:
           - Conceitos técnicos importantes
           - Aplicações práticas de IA e agentes
           - Tendências emergentes na área
           - Desafios e limitações atuais
        3. Inclua insights únicos ou exemplos práticos mencionados
        4. Destaque citações impactantes de especialistas, se houver
        
        Formate seu resumo de forma organizada com:
        - Título descritivo para cada podcast resumido
        - Lista de pontos-chave com marcadores
        - Seção de conclusões ou insights principais sobre o futuro da IA e dos agentes
        
        Mantenha o resumo conciso, informativo e focado em conteúdo de alta qualidade sobre IA e Agentes de IA.
        Se uma transcrição não contiver informações relevantes sobre IA, indique isso claramente.
        """,
        description="Agente que resume transcrições de podcasts de forma estruturada com foco em IA",
    )

    try:
        print(f"Enviando {len(transcripts_text)} caracteres para o agente resumidor...")
        entrada_do_agente = f"Aqui estão as transcrições para resumir, focando em conteúdo sobre IA e Agentes de IA:\n\n{transcripts_text}"
        resumos = call_agent(resumidor, entrada_do_agente)
        
        if not resumos or len(resumos.strip()) < 100:
            print("⚠️ O agente resumidor retornou um conteúdo muito curto ou vazio")
            return "Não foi possível gerar resumos adequados das transcrições."
            
        print(f"✅ Resumos gerados com sucesso ({len(resumos)} caracteres)")
        return resumos
    except Exception as e:
        print(f"❌ Erro ao gerar resumos: {str(e)}")
        return "Ocorreu um erro ao gerar os resumos das transcrições."
