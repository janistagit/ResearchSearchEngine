from bs4 import BeautifulSoup
from pymongo import MongoClient
from crawler import connectDataBase

db = connectDataBase()
index = db.index

# Text transformation/parsing code

# Index management code
def createDocument(col):
    termCount = {}

    document = {}

    col.insert_one(document)

def deleteDocument(col):
    pass

def updateDocument(col):
    pass

def getIndex(col):
    pass