from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
from crawler import connectDataBase 
import re

# db = connectDataBase()
# index = db.index
#the above didnt work for me
DB_HOST = 'localhost:27017'   
try:
    client = MongoClient(host=[DB_HOST])
    db = client.searchengine
    pagecollection = db['pages']
    index = db['index']
    print("connected")
except:
    print("Database not connected")
    
    

# Input: dictionary where {term : [docId, docId, docId, ...]}
# docId comes from the collection of pages (each page is a document)
def createIndexTerm(col, id, termDictionary):
    # k is the key of the dictionary (term)
    # v is the value of the dictionary (list of document IDs)
    for k, v in termDictionary.items():
        indexTerm = {
            "_id" : ObjectId(), #changed this cause i was getting an error about duplicate ids
            "term" : k,
            "docs" : v
        }

        col.insert_one(indexTerm)

def updateIndexTerm():
    pass

def deleteTerm(term):
    index.delete_one({"term": term})

# Text transformation/parsing code  

#queries the data base to find links that are need for this part
query = {'url': {'$regex': "^https:\/\/www\.cpp\.edu\/faculty\/.*\/index\.shtml$"}}

links = list(pagecollection.find(query))
#lists to hold words and ids
text = []
textwid = []
#stemming and stopping
swords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
#looping through the links we found in the query and getting the html and extracting text
#text is then processed and cleaned from things we dont want: text transformation begins
for link in links:
    docid = link['_id']
    html = link['html']
    bs = BeautifulSoup(html, 'html.parser')
    diva = bs.find_all('div', class_= 'accolades')
    for div in diva:
        t = div.get_text().replace('Â', '').replace(u'\xa0', '').replace('\n', ' ').replace('\t', '')
        cleantxt = re.sub(r'https?://[^\s,]+', '', t)
        cleantxt = re.sub(r'\b\w{3,}\.', lambda match: match.group(0)[:-1], cleantxt)  
        cleantxt = re.sub(r'[a-z]{1,2}\.$', '', cleantxt)
        cleantxt = re.sub(r'(?<!\w)-|-(?!\w)', '', cleantxt)
        cleantxt = re.sub(r'[“”"(),*:&]', '', cleantxt)
        cleantxt = cleantxt.split()
        cleantxt = [word.lower() for word in cleantxt if word.lower() not in swords]  
        cleantxt = [lemmatizer.lemmatize(word) for word in cleantxt]
        text.append(cleantxt)
        textwid.append([docid]+[cleantxt])

#print(textwid) | checking
allwords = list(set(word for doc in text for word in doc))
# print("all in one list:") | checking

for word in allwords:
    doclist = [] #list of documents where term is found
    useddocs = [] #list of already accounted for documents
    for item in textwid:
        if word in item[1] and item[0] not in useddocs: 
            doclist.append(item[0])
            useddocs.append(item[0]) 
    
    termdict = {word: doclist} #function below takes in the third variable as a dict so we make one with word and doclist
    createIndexTerm(index,word, termdict)

