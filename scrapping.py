import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import csv
import os
from difflib import SequenceMatcher


def calc_similarity(str1, str2):
    """
    Calculates the similarity between two strings.

    Parameters:
        str1 (str): The first string.
        str2 (str): The second string.

    Returns:
        float: The similarity coefficient between the two strings.

    """
    str1 = str1.strip()
    str2 = str2.strip()
    seq_matcher = SequenceMatcher(None, str1.lower(), str2.lower())
    return seq_matcher.ratio()


def get_paper_titles(url):
    """
    Retrieves the titles of articles from a web page.

    Parameters:
        url (str): The URL of the web page.

    Returns:
        list: A list of dictionaries containing the titles and authors of the articles.

    """
    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful or not
    if response.status_code == 200:
        print('The request was successful')
    else:
        print('An error occurred while making the request')

    # Get the HTML content from the response
    html = BeautifulSoup(response.text, 'html.parser')

    # Find all <font> elements in the HTML
    titles = html.find_all('font')

    # Initialize a list to store the articles
    papers = []

    # Iterate over the found titles
    for title in titles:
        # Find the <b> element that contains the article title
        text = title.find('b')

        # Find the <i> element that contains the article author
        author = title.find('i')

        # Find all <a> elements that contain related links for the article
        scholar = title.find_all('a')

        # Check if the title is not empty and not equal to unwanted values
        if text and text.text.strip() not in ['Abstract:', '[pdf] [scholar]']:
            # Clean and format the article title
            title_paper = text.text.replace("\x92", "'").replace(
                "\r", " ").replace("\n", " ")

            # Clean and format the article author
            author = author.text.replace("\x92", "'").replace(
                "\r", " ").replace("\n", " ")

            # Add the article to the list
            papers.append({
                'title': title_paper,
                'title_google': '-',
                'author_google': '-',
                'cited_by': '0',
                'author': author
            })

    # Return the list of articles
    return papers


def search_paper_info(paper_title, api_key):
    """
    Searches for information about a paper using the Google Scholar API.

    Parameters:
        paper_title (str): The title of the paper.
        api_key (str): The API key for accessing the Google Scholar API.

    Returns:
        dict or None: A dictionary containing information about the paper if a match is found, or None if no match is found.

    """
    # Set the parameters for the API request
    params = {
        "engine": "google_scholar",
        "q": paper_title,
        "api_key": api_key
    }

    # Create a GoogleSearch instance with the parameters
    search = GoogleSearch(params)

    # Perform the search and retrieve the results as a dictionary
    results = search.get_dict()

    # Get the organic search results
    organic_results = results["organic_results"]

    # Check if there are any organic search results
    if len(organic_results) > 0:
        # Iterate over the organic results
        for result in organic_results:
            # Calculate the similarity between the result title and the paper title
            similarity = calc_similarity(result["title"], paper_title)

            # Check if the similarity is above a threshold (e.g., 0.8)
            if similarity > 0.8:
                # Return the matching result
                return result

    # If no match is found, return None
    return None


def write_paper_info_to_file(filename, name, papers, api_key):
    """
    Writes paper information to a file in CSV format.

    Parameters:
        filename (str): The directory path where the file will be created.
        name (str): The name of the file (without extension).
        papers (list): A list of dictionaries containing paper information.
        api_key (str): The API key for accessing the Google Scholar API.

    Returns:
        None

    """
    # Construct the file path
    path_file = filename + "/" + name + ".csv"

    # Open the file in write mode
    with open(path_file, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['title', 'title_google', 'author',
                        'author_google', 'cited_by', 'observation'])

        # Iterate over the papers
        for dictionary in papers:
            title = dictionary.get('title')
            title_google = dictionary.get('title_google')
            author = dictionary.get('author')
            author_google = dictionary.get('author_google')
            cited_by = dictionary.get('cited_by')
            observation = '-'

            # Search for additional paper information using the Google Scholar API
            paper_info = search_paper_info(title, api_key)

            if paper_info:
                # Update the title and author information from the API response
                author_google = paper_info["publication_info"]["summary"]
                title_google = paper_info["title"]

                try:
                    cited_by = paper_info["inline_links"]["cited_by"]["total"]
                except KeyError:
                    cited_by = 0
            else:
                observation = 'not found'

            # Write a row of data to the CSV file
            writer.writerow([title, title_google, author,
                            author_google, cited_by, observation])


def create_directory(file_name="csv"):
    """
    Creates a directory with the specified name if it doesn't exist.

    Parameters:
        file_name (str): The name of the directory to be created (default is 'csv').

    Returns:
        None

    """
    # Set the folder name
    folder_name = file_name

    # Construct the folder path using the current working directory and the folder name
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Check if the folder already exists
    if os.path.exists(folder_path):
        print("The folder already exists")
    else:
        # Create the folder if it doesn't exist
        os.mkdir(folder_path)

conferences_years = ['WER00']

# Constantes
CONFERENCE_URL = 'http://wer.inf.puc-rio.br/WERpapers/papers_by_conference.lp?conference='
API_KEY = ''
FILE_NAME = 'csv'

for name in conferences_years:
    conference_url = CONFERENCE_URL + name
    papers = get_paper_titles(conference_url)
    create_directory(FILE_NAME)
    write_paper_info_to_file(FILE_NAME, name, papers, API_KEY)
