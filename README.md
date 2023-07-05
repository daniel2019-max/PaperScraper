# Conference Paper Information Web Scraper

This Python script is a web scraper that utilizes the `requests`, `BeautifulSoup` and `serpapi` libraries to fetch information about conference papers from the WER (Workshop on Requirements Engineering) event website.
The main objective of the script is to retrieve the titles and authors of conference papers and search for additional information about each paper using the Google Scholar API. The obtained information is then saved into CSV files.

# Requirements
Before running the script, make sure you have the following libraries installed:
- requests
- BeautifulSoup
- serpapi
- csv
- os
- difflib
Additionally, you'll need a valid Google Scholar API key to access the API.

# How to Use the Script
1. Configure the constants:
   - `CONFERENCE_URL`: URL of the WER conference website followed by the corresponding year.
   - `API_KEY`: Your Google Scholar API key.
   - `FILE_NAME`: Name of the directory and CSV file where the results will be saved.
2. Execute the script:
   - Run the "scrapping.py" script and wait for the execution to complete.
   - During execution, console messages will indicate whether the requests were successful or if any errors occurred.
3. Results:
   - After execution, a directory named `csv` (or the name you specified in `FILE_NAME`) will be created in the same directory as the script.
   - Within the directory, a CSV file will be generated for each conference year specified in the `conferences_years` list.
     
# Considerations
- This script utilizes web scraping techniques to extract information from a website. Make sure to comply with the policies and terms of use of the website from 
  which information is being extracted.
- The accuracy of the results may vary depending on the availability and accuracy of information on the website and the Google Scholar API.
- You may need to make additional adjustments to the script to fit your specific requirements.
