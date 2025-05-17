# 🎙️ Podcast Generator: Sistema Multi-Agente com Gemini

![Banner Podcast Generator](https://img.shields.io/badge/🎙️%20Podcast%20Generator-Imersão%20IA%20Alura-6F57FF?style=for-the-badge)

Um sistema de geração de podcasts baseado em múltiplos agentes de IA, desenvolvido durante a Imersão IA &amp; Agents da Alura usando o SDK do Google para Gemini Agents.

[![Python Badge](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](#)
[![Google Gemini Badge](https://img.shields.io/badge/Google%20Gemini-886FBF?style=flat-square&logo=google&logoColor=white)](#)
[![YouTube API Badge](https://img.shields.io/badge/YouTube%20API-FF0000?style=flat-square&logo=youtube&logoColor=white)](#)

## 📋 Índice

- [🎙️ Podcast Generator: Sistema Multi-Agente com Gemini](#️-podcast-generator-sistema-multi-agente-com-gemini)
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
  - [👤 Autor](#-autor)

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio da Imersão IA &amp; Agents da Alura. A ideia central é usar a tecnologia de agentes de IA do Google (Gemini Agents) para automatizar a criação de conteúdo para podcasts sobre temas de tecnologia, particularmente IA.

O sistema utiliza uma arquitetura de múltiplos agentes especializados que trabalham em conjunto para:
1. Descobrir podcasts relevantes no YouTube
2. Obter e processar suas transcrições
3. Resumir o conteúdo extraindo os pontos-chave
4. Sintetizar um novo roteiro de podcast original

## ✨ Características

- 🔍 **Busca Inteligente**: Encontra os podcasts mais relevantes e recentes sobre um tópico específico
- 📝 **Transcrição Automática**: Obtém transcrições de vídeos do YouTube em português e inglês
- 📊 **Resumo Avançado**: Extrai os pontos-chave e insights mais importantes de cada fonte
- 📚 **Síntese Criativa**: Gera um script completo para um novo podcast, estruturado e pronto para gravação
- 💾 **Exportação em Markdown**: Salva o script final em formato Markdown para fácil edição

## 🔄 Arquitetura de Agentes

O sistema utiliza quatro agentes especializados que trabalham em sequência:

![Diagrama de Arquitetura](https://img.shields.io/badge/-Arquitetura%20Multi--Agente-informational?style=flat-square)

1. **Agente Buscador** 🔎
   - Modelo: `gemini-2.0-flash`
   - Função: Buscar podcasts relevantes no YouTube sobre o tópico especificado
   - Ferramentas: Google Search Tool

2. **Agente Transcritor** 🎯
   - Biblioteca: `youtube-transcript-api`
   - Função: Obter transcrições dos vídeos encontrados
   - Capacidades: Processa transcrições em PT-BR e EN

3. **Agente Resumidor** 📝
   - Modelo: `gemini-2.5-pro-preview-03-25`
   - Função: Analisar e resumir as transcrições em pontos-chave
   - Foco: Extrair informações essenciais e insights de valor

4. **Agente Sintetizador** 🎙️
   - Modelo: `gemini-2.5-pro-preview-03-25`
   - Função: Sintetizar um roteiro de podcast original e coerente
   - Estrutura: Introdução, Desenvolvimento por tópicos, Conclusão

## 📦 Requisitos e Instalação

### Pré-requisitos:

- Python 3.8+
- Acesso à API do Google Gemini
- Conexão com internet

### Instalação:

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/podcast-generator.git
cd podcast-generator
```

2. Instale as dependências:
```bash
pip install google-generativeai dotenv youtube-transcript-api
```

3. Configure sua chave de API:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API: `GOOGLE_API_KEY=sua_chave_aqui`

## 🎯 Como Usar

1. Execute o script principal:
```bash
python podcast_generator.py
```

2. Digite o tópico desejado para o podcast quando solicitado (exemplo: "IA e Agents de IA")

3. O sistema vai executar automaticamente:
   - Buscando podcasts relevantes
   - Obtendo transcrições
   - Resumindo o conteúdo
   - Gerando o script do podcast

4. O resultado final será exibido na tela e salvo em um arquivo markdown.

## 🛠️ Tecnologias Utilizadas

- **Google ADK for Agents**: Framework para criação e gerenciamento de agentes de IA
- **Google Gemini Models**: Modelos de IA utilizados pelos agentes (2.0-flash e 2.5-pro)
- **Youtube Transcript API**: Para extração de legendas/transcrições de vídeos
- **Python**: Linguagem de programação principal
- **Markdown**: Formato de saída para scripts gerados

## 🧠 Aprendizados

Este projeto demonstra:

- Como criar sistemas complexos utilizando múltiplos agentes especializados
- Técnicas para orquestrar o fluxo de informações entre agentes
- Uso prático do SDK Gemini para agents em um cenário real
- Aplicação de LLMs na geração de conteúdo estruturado
- Integração com APIs externas para enriquecimento de dados

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

Desenvolvido como parte do desafio da Imersão IA &amp; Agents da Alura.

---

<p align="center">
  <small>Feito com ❤️ utilizando Gemini e os conhecimentos da Imersão IA &amp; Agents Alura</small>
</p>