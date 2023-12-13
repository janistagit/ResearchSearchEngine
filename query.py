from pymongo import MongoClient
from bson import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
#from crawler import connectDataBase

def connect_to_database():
    client = MongoClient()
    db = client.searchengine
    return db

def search_index(query, indexes):
    index_info = []
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    index_terms = list(indexes.find())
    all_terms = [term['term'] for term in index_terms]
    tfidf_vectorizer.fit(all_terms)
    #print(tfidf_vectorizer.idf_)

    query_matrix = tfidf_vectorizer.fit_transform([query])
    #print(query_matrix)
    term_texts = [term['term'] for term in index_terms if term['term']]
    term_matrix = tfidf_vectorizer.transform(term_texts)
    print(term_matrix)
    
    for term, term_doc in zip(index_terms, term_matrix):
        term_text = term['term']
        if term_text:
            similarity = cosine_similarity(query_matrix, term_doc).flatten()[0]
            index_info.append({'term': term_text, 'similarity': similarity, 'docs': term['docs']})

    index_info.sort(key=lambda x: x['similarity'], reverse=True)
    doc_info_list = [(doc_id, similarity) for doc_info in index_info for doc_id in doc_info['docs'] for similarity in [doc_info['similarity']]]
    return doc_info_list




def retrieve_documents(doc_info_list, pages_collection):
    # grab the associated docs with the id
    documents = list(pages_collection.find({'_id': {'$in': [ObjectId(doc_id) for doc_id, _ in doc_info_list]}}))
    return zip(doc_info_list, documents)

def pagination(results, page_size):
    result_list = list(results)

    total_item_count = len(result_list)
    total_pages = (total_item_count + page_size - 1) // page_size

    while True:
        try:
            page_number = int(input("Enter page number or -1 to exit: "))

            if page_number == -1:
                break

            if 1 <= page_number <= total_pages:
                start_index = (page_number - 1) * page_size
                end_index = page_number * page_size
                page_data = result_list[start_index:end_index]
                print(f"Page: {page_number}")
                for (doc_id, similarity), result in page_data:
                    url = result.get('url')
                    html_content = result.get('html', '')
                    if html_content:
                        soup = BeautifulSoup(html_content, 'html.parser')
                        h1_tag = soup.find('h1')
                        h1_text = h1_tag.get_text()
                        print(f"URL: {url}")
                        print(f"{h1_text}")
                        print(f"Cosine Similarity: {similarity}")
                        print("\n")
                    else:
                        print("No HTML content found.")
            else:
                print("Not a valid page number. Please try again.")
                print()
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            print()

query = input("Search query: ")
#db, client = connectDataBase() makes it run crawler
db = connect_to_database()
doc_info_list = search_index(query, db.index)
pages_collection = db.pages
results = retrieve_documents(doc_info_list, pages_collection)
pagination(results, page_size=5)