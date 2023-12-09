from bs4 import BeautifulSoup
from pymongo import MongoClient
from crawler import connectDataBase
import re

db = connectDataBase()
index = db.index

# Text transformation/parsing code

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
