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