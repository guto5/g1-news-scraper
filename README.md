## Sobre as bibliotecas utilizadas no projeto

```bash
from pathlib import Path  # Facilita o uso de caminhos relativos e absolutos
import json               # Usado para serializar os dados no formato JSON
import pandas as pd       # Gera e exporta os dados para um arquivo Excel
from loguru import logger # Facilita o logging com uma sintaxe simples
from playwright.sync_api import sync_playwright  # Faz scraping usando um navegador headless
from openpyxl import load_workbook  # Ajusta a formatação do Excel


## Como rodar o projeto

# Foi utilizada a versão 3.11.9 do Python, pois ela é compatível com todas as bibliotecas utilizadas no projeto

# Clone o repositório e acesse a pasta
git clone https://github.com/seu-usuario/g1-news-scraper.git
cd g1-news-scraper

# Crie e ative o ambiente virtual
python3 -m venv .venv # (python -m venv .venv)
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# Instale as dependências do projeto
pip install -r requirements.txt

# Instale o navegador necessário para o Playwright
python -m playwright install chromium

# Execute o script principal
python src/main.py

# g1-news-scraper
