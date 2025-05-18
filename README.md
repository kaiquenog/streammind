# 🎙️ StreamMind: Sistema Multi-Agente Gerador de Podcasts

![Banner StreamMind](https://img.shields.io/badge/🎙️%20StreamMind-Imersão%20IA%20Alura-6F57FF?style=for-the-badge)

Um sistema de geração de podcasts baseado em múltiplos agentes de IA, desenvolvido durante a Imersão IA &amp; Agents da Alura usando o SDK do Google para Gemini Agents.

[![Python Badge](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](#)
[![Google Gemini Badge](https://img.shields.io/badge/Google%20Gemini-886FBF?style=flat-square&logo=google&logoColor=white)](#)
[![YouTube API Badge](https://img.shields.io/badge/YouTube%20API-FF0000?style=flat-square&logo=youtube&logoColor=white)](#)

## 📋 Índice

- [🎙️ StreamMind: Sistema Multi-Agente Gerador de Podcasts](#️-streammind-sistema-multi-agente-gerador-de-podcasts)
  - [📋 Índice](#-índice)
  - [🚀 Sobre o Projeto](#-sobre-o-projeto)
  - [✨ Características](#-características)
  - [🔄 Arquitetura de Agentes](#-arquitetura-de-agentes)
  - [📦 Requisitos e Instalação](#-requisitos-e-instalação)
    - [Pré-requisitos:](#pré-requisitos)
    - [Instalação:](#instalação)
  - [🎯 Como Usar](#-como-usar)
  - [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
  - [🧠 Aprendizados](#-aprendizados)
  - [📝 Licença](#-licença)
  - [👤 Autor](#-autor)s

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio da Imersão IA & Agents da Alura. A proposta é utilizar agentes inteligentes com o SDK do Gemini para automatizar a curadoria e síntese de conteúdos sobre Inteligência Artificial disponíveis em vídeos do YouTube. O sistema busca vídeos populares e recentes sobre IA, transcreve e resume os conteúdos, e por fim, gera um novo podcast com os principais insights, facilitando a atualização sobre o tema de forma rápida e acessível.

### 🎯 Objetivo Final

O objetivo final deste projeto era criar uma experiência similar ao NotebookLM da Google - uma ferramenta que não apenas gera conteúdo textual, mas também o converte em áudio, o objetivo final é de criar um podcast com qualidade profissional. Este objetivo ainda não foi alcançado com a implementação da síntese de voz usando a biblioteca gTTS (Google Text-to-Speech), que converte o script gerado em um arquivo de áudio MP3.

O sistema utiliza uma arquitetura de múltiplos agentes especializados que trabalham em conjunto para:
1. Descobrir podcasts relevantes no YouTube
2. Extrair e processar suas transcrições
3. Resumir os principais insights
4. Sintetizar um novo script de podcast original
5. Converter o script em áudio usando síntese de voz de podcast

## ✨ Características

- 🔍 **Busca Inteligente Aprimorada**: Encontra os podcasts mais relevantes sobre um tópico específico usando múltiplas estratégias de busca
- 📝 **Transcrição Automática Multilíngue**: Obtém transcrições de vídeos do YouTube em português, inglês e outros idiomas disponíveis
- 📊 **Resumo Avançado Focado**: Extrai os pontos-chave e insights mais importantes de cada fonte com foco em IA e Agentes
- 📚 **Síntese Criativa Estruturada**: Gera um script completo para um novo podcast, com seções bem definidas e conteúdo coeso
- 💾 **Exportação em Markdown**: Salva o script final em formato Markdown para fácil edição
- 🔊 **Síntese de Voz**: Converte o script em áudio de podcast usando gTTS (Google Text-to-Speech)

## 🔄 Arquitetura de Agentes

O sistema utiliza cinco agentes especializados que trabalham em sequência, cada um em seu próprio módulo Python:

![Diagrama de Arquitetura](https://img.shields.io/badge/-Arquitetura%20Multi--Agente-informational?style=flat-square)

1. **Agente Buscador** (`youtube_search_agent.py`) 🔎
   - Modelo: `gemini-2.5-pro-preview-03-25`
   - Função: Buscar podcasts relevantes no YouTube sobre o tópico especificado
   - Ferramentas: Google Search Tool
   - Estratégia: Utiliza múltiplas consultas para maximizar resultados relevantes

2. **Agente Transcritor** (`transcription_agent.py`) 🎥
   - Biblioteca: `youtube-transcript-api`
   - Função: Obter transcrições dos vídeos encontrados
   - Capacidades: Processa transcrições em PT-BR, EN e outros idiomas disponíveis
   - Tratamento de erros: Lida com vídeos indisponíveis ou sem transcrições

3. **Agente Resumidor** (`summary_agent.py`) 📝
   - Modelo: `gemini-2.5-pro-preview-03-25`
   - Função: Analisar e resumir as transcrições em pontos-chave
   - Foco: Extrair informações essenciais e insights de valor sobre IA e Agentes
   - Limitação: Gerencia o tamanho do conteúdo para evitar exceder limites de contexto

4. **Agente Sintetizador** (`synthesis_agent.py`) 🎤
   - Modelo: `gemini-2.5-pro-preview-03-25`
   - Função: Sintetizar um roteiro de podcast original e coerente
   - Estrutura: Título, Introdução, Desenvolvimento, Tendências e Futuro, Conclusão
   - Metadados: Adiciona informações como data de geração ao script final

5. **Agente Sintetizador de Voz** (`speech_synthesis_agent.py`) 🔊
   - Função: Converter o script do podcast em áudio
   - Status: Implementado e funcional
   - Recursos avançados: Utiliza pydub e ffmpeg para criar transições, introdução e conclusão
   - Integração: Utiliza a biblioteca gTTS (Google Text-to-Speech) para gerar arquivos MP3
   - Tratamento de erros: Detecta automaticamente se ffmpeg está instalado e oferece uma versão simplificada quando não está disponível

## 📦 Requisitos e Instalação

### Pré-requisitos:

- Python 3.8+
- Acesso à API do Google Gemini
- Conexão com internet
- ffmpeg (para recursos avançados de áudio)

### Instalação:

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/podcast-generator.git
cd podcast-generator
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Instale o ffmpeg (opcional, mas recomendado para recursos avançados de áudio):
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - macOS (com Homebrew): `brew install ffmpeg`
   - Windows: Baixe do site oficial ou use o gerenciador de pacotes Chocolatey

4. Configure sua chave de API:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API: `GOOGLE_API_KEY=sua_chave_aqui`

## 🎯 Como Usar

1. Execute o script principal refatorado:
```bash
python main.py
```

2. Digite o tópico desejado para o podcast quando solicitado (exemplo: "IA e Agents de IA")

3. O sistema vai executar automaticamente:
   - Buscando podcasts relevantes usando múltiplas consultas
   - Obtendo transcrições em vários idiomas
   - Resumindo o conteúdo com foco em IA e Agentes
   - Gerando o script estruturado do podcast
   - Convertendo o script em áudio de podcast com formato profissional

4. O resultado final (script e áudio) será exibido na tela e salvo em arquivos markdown e MP3.

5. Recursos avançados de áudio (quando ffmpeg está instalado):
   - Introdução e conclusão profissionais
   - Divisão do podcast em seções com anúncios de transição
   - Pausas apropriadas entre seções para melhor ritmo
   - Detecção automática de título e estrutura do podcast

6. Estrutura do projeto:
```
streamMind/
├── agents/               # Pasta com os agentes individuais
│   ├── __init__.py
│   ├── youtube_search_agent.py   # Agente de busca no YouTube
│   ├── transcription_agent.py    # Agente de transcrição
│   ├── summary_agent.py         # Agente de resumo
│   ├── synthesis_agent.py       # Agente de síntese de script
│   └── speech_synthesis_agent.py # Agente de síntese de voz
├── utils/                # Utilitários compartilhados
│   ├── __init__.py
│   ├── common.py              # Funções comuns (extract_video_id, etc)
│   └── agent_communication.py   # Funções para comunicação com agentes
├── main.py              # Script original
└── README.md            # Documentação
```

## 🔧️ Tecnologias Utilizadas

- **Google ADK for Agents**: Framework para criação e gerenciamento de agentes de IA
- **Google Gemini Models**: Modelos de IA utilizados pelos agentes (gemini-2.5-pro-preview e gemini-2.0-flash)
- **Youtube Transcript API**: Para extração de legendas/transcrições de vídeos em múltiplos idiomas
- **Python**: Linguagem de programação principal com arquitetura modular
- **Markdown**: Formato de saída para scripts gerados
- **gTTS (Google Text-to-Speech)**: Utilizado para converter o texto do podcast em áudio MP3
- **pydub**: Biblioteca para processamento avançado de áudio e criação de transições
- **ffmpeg**: Ferramenta para manipulação de áudio e vídeo, utilizada pelo pydub
- **NotebookLM (Referência)**: Inspiração para o objetivo final de geração de áudio de podcast com qualidade profissional

## 🧠 Aprendizados

Este projeto demonstra:

- Como criar sistemas complexos utilizando múltiplos agentes especializados
- Arquitetura modular para melhor organização e manutenção do código
- Separação de responsabilidades com cada agente em seu próprio módulo
- Técnicas para orquestrar o fluxo de informações entre agentes
- Uso prático do SDK Gemini para agents em um cenário real
- Aplicação de LLMs na geração de conteúdo estruturado
- Integração com APIs externas para enriquecimento de dados
- Tratamento de erros robusto em cada etapa do processo
- Detecção automática de dependências do sistema (ffmpeg)
- Implementação de mecanismos de fallback para garantir funcionalidade básica
- Processamento avançado de áudio para criação de podcasts com qualidade profissional
- Adaptação dinâmica baseada nos recursos disponíveis no ambiente de execução

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

Desenvolvido como parte do desafio da Imersão IA &amp; Agents da Alura.
[Kaique Nogueira](https://www.linkedin.com/in/kaique-nogueira-b11b345b/)

---

<p align="center">
  <small>Feito com ❤️ utilizando Gemini e os conhecimentos da Imersão IA &amp; Agents Alura</small>
</p>