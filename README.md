# IA integrada a fontes externas

Aplicação em Python com Streamlit para combinar respostas factuais de fontes externas com interpretação gerada por um modelo local do Ollama. O projeto demonstra como uma IA pode consultar dados confiáveis de APIs e bancos locais, separar a resposta factual da explicação da IA e manter o contexto visível ao usuário.

## Visão geral

A interface permite:

- consultar a temperatura e condições climáticas de cidades brasileiras via Open-Meteo;
- consultar um catálogo de produtos salvo em SQLite;
- ativar uma explicação produzida por um modelo local do Ollama;
- visualizar a resposta factual e a interpretação da IA de forma separada;
- inspecionar os dados brutos usados como contexto da consulta.

## Funcionalidades

- `Streamlit` para a interface de conversa;
- `SQLite` para armazenar produtos iniciais e consultas locais;
- `Open-Meteo` para geocodificação e dados climáticos em tempo real;
- `Ollama` para gerar interpretações em texto usando modelos locais;
- tratamento de recusas indevidas e exibição da fonte consultada.

## Estrutura do projeto

- `app.py`: interface principal e fluxo da aplicação;
- `config.py`: configuração de caminhos e endereço do Ollama;
- `services/database.py`: inicialização do banco SQLite e consultas de produtos;
- `services/weather.py`: geocodificação e consulta meteorológica;
- `services/ollama.py`: detecção de modelos ativos e geração de texto;
- `services/responses.py`: formatação das respostas factuais e validação de recusas;
- `aula6.db`: banco SQLite gerado automaticamente com dados iniciais de produtos.

## Pré-requisitos

- Python 3.10+
- `pip`
- Ollama instalado e em execução
- Modelos locais do Ollama disponíveis para interpretação textual

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Execução

1. Verifique se o Ollama está ativo:

```bash
ollama ps
```

2. Se necessário, carregue um modelo em outro terminal:

```bash
ollama run NOME_DO_MODELO
```

3. Inicie a aplicação:

```bash
streamlit run app.py
```

## Como usar

- No painel lateral, escolha a fonte da consulta:
  - `API de clima`
  - `Banco de produtos`
- Para clima, informe uma cidade brasileira e permita a interpretação com IA se quiser uma explicação em linguagem natural.
- Para produtos, selecione uma categoria e, opcionalmente, habilite a explicação da IA.
- A aplicação exibe:
  - a resposta factual obtida diretamente da fonte;
  - a interpretação do modelo, quando disponível;
  - o modelo utilizado;
  - a fonte consultada;
  - os dados brutos usados como contexto.

## Observações importantes

- A consulta factual funciona mesmo sem Ollama.
- A interpretação da IA aparece separada da resposta direta da fonte para manter a informação factual clara.
- Se nenhum modelo estiver carregado, a interface informa isso e continua mostrando apenas a resposta baseada em dados externos.

## Objetivo do projeto

Este repositório serve como exemplo prático de arquitetura modular para aplicações de IA que acessam fontes externas de forma controlada, com foco em transparência, rastreabilidade e separação entre dados factuais e inferência da IA.
