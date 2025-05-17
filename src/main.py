from pathlib import Path
import json
import pandas as pd
from loguru import logger
from playwright.sync_api import sync_playwright
from openpyxl import load_workbook

# Define a rota dos arquivos JSON/EXCEL no root do projeto
OUTPUT_JSON  = Path(__file__).parent.parent / "noticia.json"
OUTPUT_EXCEL = Path(__file__).parent.parent / "noticias.xlsx"
URL = "https://g1.globo.com/"

# Realiza o scraping da última notícia exibida na página inicial do G1
def scrape_latest_news(post_selector="div.feed-post"):
    with sync_playwright() as p:
        logger.info("Abrindo navegador")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        # Aguarda o javascript da pagina ser carregado
        page.wait_for_selector(post_selector, timeout=15000)

        # Extrai o título, data de publicação e resumo da notícia mais recente do G1
        post = page.query_selector(post_selector)
        titulo  = post.query_selector("a.feed-post-link").inner_text().strip()
        data    = post.query_selector("span.feed-post-datetime").inner_text().strip()
        resumo_el = post.query_selector("div.bstn-related") or post.query_selector("div.feed-post-body-resumo")
        
        resumo = resumo_el.inner_text().strip() if resumo_el else ""

        browser.close()
        return {"titulo": titulo, "data_publicacao": data, "resumo": resumo}

# Salva os arquivos JSON/EXCEL
def save_files(dados: dict):
    logger.info("Salvando JSON em {}", OUTPUT_JSON)
    OUTPUT_JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2))

    logger.info("Salvando Excel em {}", OUTPUT_EXCEL)

    # Converte os dados para DataFrame
    noticia_dataframe = pd.DataFrame([dados])
    noticia_dataframe.to_excel(OUTPUT_EXCEL, index=False)

    # Ajusta largura das colunas proporcional ao conteúdo
    workbook = load_workbook(OUTPUT_EXCEL)
    planilha = workbook.active

    for coluna in planilha.columns:
        comprimento_maximo = 0
        letra_coluna = coluna[0].column_letter

        for celula in coluna:
            if celula.value:
                comprimento_maximo = max(comprimento_maximo, len(str(celula.value)))

        largura_ajustada = comprimento_maximo + 1
        planilha.column_dimensions[letra_coluna].width = largura_ajustada

    workbook.save(OUTPUT_EXCEL)


def main():
    logger.info("Iniciando scrape na página inicial do G1")
    noticia = scrape_latest_news()
    save_files(noticia)
    logger.success("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
