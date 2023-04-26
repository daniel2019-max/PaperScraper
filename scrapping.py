import requests
from bs4 import BeautifulSoup
from scholarly import scholarly, ProxyGenerator
from serpapi import GoogleSearch


def get_paper_titles(url):
    response = requests.get(url)

    if response.status_code == 200:
        print('La solicitud fue exitosa')
    else:
        print('Ocurrió un error al realizar la solicitud')

    html = BeautifulSoup(response.text, 'html.parser')
    titles = html.find_all('font')
    papers = []

    for title in titles:
        text = title.find('b')
        if text and text.text.strip() not in ['Abstract:', '[pdf] [scholar]']:
            papers.append(text.text.replace("\x92", "'").replace(
                "\r", " ").replace("\n", " "))

    return papers


def search_paper_info(paper_title, api_key):
    params = {
        "engine": "google_scholar",
        "q": paper_title,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    if len(organic_results) > 1:
        for result in organic_results:
            if result["title"] == paper_title:
                return result
    elif len(organic_results) == 1:
        return organic_results[0]

    return None


def write_paper_info_to_file(name, papers, api_key):
    with open(name + ".txt", "w", encoding='utf-8') as file:
        for paper_title in papers:
            print('papper', paper_title)
            paper_info = search_paper_info(paper_title, api_key)

            if paper_info:
                file.write(f'Título: {paper_info["title"]}\n')
                file.write(
                    f'Resumen: {paper_info["publication_info"]["summary"]}\n')

                try:
                    citations = paper_info["inline_links"]["cited_by"]["total"]
                except KeyError:
                    citations = 0

                file.write(f'Citas: {citations}\n')
            else:
                file.write(
                    f'No se encontraron resultados para el paper "{paper_title}"\n\n')
            file.write(
                f'-------------------------------------------------------------------')


# Configuración de proxy
pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

conferences_years = ['WER02', 'WER01', 'WER00','WER99', 'WER98']

# ojo con wer18
# Constantes
CONFERENCE_URL = 'http://wer.inf.puc-rio.br/WERpapers/papers_by_conference.lp?conference='
API_KEY = '5081c63ec9677ada462bf8ba8ce9d818cf580173f1602ffb79e0afc097caa05f'


for year in conferences_years:
    conference_url = CONFERENCE_URL + year
    papers = get_paper_titles(conference_url)
    write_paper_info_to_file(year, papers, API_KEY)
