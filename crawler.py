from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

# connect to mongoDB database
def connectDataBase():
    client = MongoClient(host="localhost", port=27017)
    db = client.searchengine
    return db

"""
Determines if target page is found based off faculty page pattern
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
                       
# Function to grab URLs, Arg HTML, returns List of Urls(string list)
def parse(html):
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find_all('a', href = True)
    return links

# Frontier class for crawling based off Queue 
class Frontier:
    def __init__(self, seed_urls):
        self.visited = set()            #keep track of visited pages
        self.queue = list(seed_urls)    #implement queue

    # add url to queue
    def add_url(self, url):
        if url not in self.visited:
            self.queue.append(url)

    # return next url in queue
    def next_url(self):
        return self.queue.pop(0) if self.queue else None

    # No more links to visit
    def done(self):
        return len(self.queue) == 0
        
    #clear list once all targets found
    def clear(self):
        self.queue.clear()
        
def crawlerThread(frontier, num_targets):
    targets_found = 0    
    while not frontier.done():
        url = frontier.next_url()
        
        try:
            html = urlopen(url)
            html = html.read()
        except URLError as e:
            print("Error server not found")
            continue
        except HTTPError as e:
            print(e)
            continue
        except Exception as e:
            print("Unknown Error")
            continue
        else:
            store_page(url, html)
            print('Crawling: ' + url)

        # once we hit minimimum of num_targets(10-20) stop crawl
        if is_target_page(html):
            targets_found += 1
            if targets_found == num_targets:
                frontier.clear()
                break
                
        for link in parse(html):
            absolute_link = urljoin(url, link)
            frontier.add_url(absolute_link)
