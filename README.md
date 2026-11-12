#AI Sales Analyst

Aplicação interativa de análise de vendas desenvolvida com Python, Streamlit, Pandas e Plotly, com integração de inteligência artificial para interpretar indicadores e responder perguntas sobre os dados comerciais.

- Objetivo

Transformar dados de vendas em informações úteis para análise de desempenho comercial, permitindo identificar tendências, acompanhar indicadores e obter insights por meio de um assistente de IA.

- Funcionalidades

Indicadores de desempenho: faturamento total, quantidade de vendas, unidades comercializadas e ticket médio.

Filtros dinâmicos: análise por período, categoria e estado.

Visualizações interativas: faturamento mensal, desempenho por categoria, produtos mais vendidos e resultados por estado.

Assistente de IA: interação em linguagem natural para consultar os dados, interpretar indicadores e obter análises comerciais.

Exportação de dados: download dos registros filtrados em CSV.

- Tecnologias

Python

Pandas

Streamlit

Plotly

Requests

OpenRouter API

NVIDIA Nemotron

Git e GitHub

- Inteligência Artificial

O projeto utiliza a API do OpenRouter para conectar o modelo NVIDIA Nemotron a um assistente integrado ao dashboard.

A aplicação processa os dados de vendas e disponibiliza indicadores e informações consolidadas para que o modelo responda perguntas e produza análises contextualizadas.

- Dados

O projeto utiliza uma base de dados fictícia com 1.000 registros de vendas, criada para demonstrar as funcionalidades da aplicação.

- Como executar

Clone este repositório:

git clone https://github.com/ArthurMonteiroCodes/AI-Sales-Analyst.git

Acesse a pasta:

cd AI-Sales-Analyst

Crie um ambiente virtual:

python -m venv .venv

Ative o ambiente virtual no Windows:

.venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Configure sua chave da API do OpenRouter no arquivo .streamlit/secrets.toml:

OPENROUTER_API_KEY = "sua-chave-aqui"

Execute a aplicação:

streamlit run app.py