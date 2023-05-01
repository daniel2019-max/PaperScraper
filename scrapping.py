import requests
from bs4 import BeautifulSoup
from scholarly import scholarly, ProxyGenerator
from serpapi import GoogleSearch
import csv
import os
from difflib import SequenceMatcher


def calc_similarity(str1, str2):
    str1 = str1.strip()
    str2 = str2.strip()
    seq_matcher = SequenceMatcher(None, str1.lower(), str2.lower())
    return seq_matcher.ratio()


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
        author = title.find('i')
        if text and text.text.strip() not in ['Abstract:', '[pdf] [scholar]']:
            title_paper = text.text.replace("\x92", "'").replace(
                "\r", " ").replace("\n", " ")
            author = author.text.replace("\x92", "'").replace(
                "\r", " ").replace("\n", " ")
            papers.append({
                'title': title_paper,
                'title_google': '-',
                'author_google': '-',
                'cited_by': '0',
                'author': author
            })
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
    if len(organic_results) > 0:
        for result in organic_results:
            similarity = calc_similarity(result["title"], paper_title)
            if similarity > 0.8:
                return result
    return None


def write_paper_info_to_file(filename, name, papers, api_key):
    path_file = filename+"/"+name+'.csv'
    with open(path_file, mode='w', newline='', encoding='utf-8') as file:
        # creamos el objeto writer
        writer = csv.writer(file)
        # escribimos una fila de datos
        writer.writerow(
            ['título', 'título google', 'autor', 'author google', 'nro citas', 'observación'])
        for dictionary in papers:
            title = dictionary.get('title')
            title_google = dictionary.get('title_google')
            author = dictionary.get('author')
            author_google = dictionary.get('author_google')
            cited_by = dictionary.get('cited_by')
            observation = '-'
            paper_info = search_paper_info(title, api_key)
            if paper_info:
                author_google = paper_info["publication_info"]["summary"]
                title_google = paper_info["title"]
                try:
                    cited_by = paper_info["inline_links"]["cited_by"]["total"]
                except KeyError:
                    cited_by = 0
            else:
                observation = 'not found'
            writer.writerow(
                [title, title_google, author, author_google, cited_by, observation])


def create_directory(file_name="csv"):
    nombre_carpeta = file_name
    ruta_carpeta = os.path.join(os.getcwd(), nombre_carpeta)
    if os.path.exists(ruta_carpeta):
        print("La carpeta existe")
    else:
        os.mkdir(ruta_carpeta)


pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

conferences_years = ['WER21']

# Constantes
CONFERENCE_URL = 'http://wer.inf.puc-rio.br/WERpapers/papers_by_conference.lp?conference='
API_KEY = 'd0808aef610cf91af1d083c8181d2f885115f904b79b9f0296fd4cfa47cc8001'
FILE_NAME = 'csv'

for name in conferences_years:
    conference_url = CONFERENCE_URL + name
    papers = get_paper_titles(conference_url)
    create_directory(FILE_NAME)
    write_paper_info_to_file(FILE_NAME, name, papers, API_KEY)
