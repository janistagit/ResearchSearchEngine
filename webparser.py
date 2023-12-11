from bs4 import BeautifulSoup
from pymongo import MongoClient
from crawler import connectDataBase
import re

#database connection doesnt work well for me
# db = connectDataBase()
# index = db.index
DB_HOST = 'localhost:27017'   
try:
    client = MongoClient(host=[DB_HOST])
    db = client.searchengine
    pagecollection = db['pages']
    print("connected")
except:
    print("Database not connected")

# Text transformation/parsing code
#what i have so far, finds links in pages through query, then in a loop, gets the id and html and finds the text and stores in text[] but before that goes in a loop for every text from inbetween the div and gets the text, replaces some annoying text stuff and splits all the words into seperate strings into text
#at the end, its to check
query = {'url': {'$regex': "^https:\/\/www\.cpp\.edu\/faculty\/.*\/index\.shtml$"}}

links = list(pagecollection.find(query))

text = []

for link in links:
    docid = link['_id']
    html = link['html']
    bs = BeautifulSoup(html, 'html.parser')
    diva = bs.find_all('div', class_= 'accolades')
    for div in diva:
        t = div.get_text().replace('Â', '').replace(u'\xa0', '').replace('\n', '').replace('\t', '').split()
        text.append(t)
        
        
for doc in text:
    print(doc)

# Input: dictionary where {term : [docId, docId, docId, ...]}
# docId comes from the collection of pages (each page is a document)
def createIndexTerm(col, id, termDictionary):
    # k is the key of the dictionary (term)
    # v is the value of the dictionary (list of document IDs)
    for k, v in termDictionary.items():
        indexTerm = {
            "_id" : id,
            "term" : k,
            "docs" : v
        }

        col.insert_one(indexTerm)

def updateIndexTerm():
    pass

def deleteTerm(term):
    index.delete_one({"term": term})
