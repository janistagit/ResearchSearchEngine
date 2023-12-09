from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def connectDataBase():
    client = MongoClient(host="localhost", port=27017)
    db = client.searchengine
    return db

# Determine if URL follows faculty page pattern
"""
Determines if target page is found
params: html (string)
returns: Found(boolean)

"""

def is_target_page(html):
    bs = BeautifulSoup(html, 'html.parser')
    
    # Check if the HTML contains the 'fac-info' division which indicates a faculty member's page
    faculty_info = soup.find('div', class_='fac-info')
    
    # Check if within 'fac-info', there's an 'h1' tag for the faculty name, 
    # and 'title-dept' class within a 'span' for the faculty title and department
    if faculty_info:
        faculty_name = faculty_info.find('h1')
        faculty_title_dept = faculty_info.find('span', class_='title-dept')
        # If both elements exist, it's likely a target page
        return bool(faculty_name and faculty_title_dept)
    return False
    
# Function to retrieve and store page in MongoDB
def store_page(url, html):
    # Store page in MongoDB: url, html
    pages_collection.insert_one({'url': url, 'html': html})

# Function to retrieve HTML content from URLs, Arg url(string), Returns HTML(string)
def retrieve_url(url):
    response = urlopen(url)
    return response.read()

# Function to grab URLs, Arg HTML, returns List of Urls(string list)
def parse(html):
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find_all('a')
    return [link.get('href') for link in links]
