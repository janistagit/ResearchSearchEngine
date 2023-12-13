from bson import ObjectId
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_html_from_id(db, doc_id):
    collection = db.pages
    document = collection.find_one({"_id": doc_id})
    return document['html'] if document else ''

def get_docs(db, term):
    collection = db.index
    index_term = collection.find_one({"term": term})
    return index_term['docs'] if index_term else []

def get_url_and_name(db, doc_id):
    collection = db.pages
    document = collection.find_one({"_id": doc_id})
    return document['url'], document['html'].split('<h1>')[1].split('</h1>')[0] if document else None

def get_doc_terms(db, doc_id):
    doc_terms = []
    docs = db.index.find({"docs": {"$elemMatch": {"$eq": ObjectId(doc_id)}}})
    for doc in docs:
        doc_terms.append(doc["term"])
    return doc_terms

def search_engine(query, db, page_size=5):
    all_index_terms = []
    # loop to get all terms
    for term in query.split():
        doc_ids = get_docs(db, term)
        print(f"term: {term}, doc ids: {doc_ids}")
        for doc_id in doc_ids:
            terms_for_document = get_doc_terms(db, doc_id)
            print(f"docId: {doc_id}, doc terms: {terms_for_document}")
            all_index_terms.extend(terms_for_document)

    if not all_index_terms:
        print("No matching documents found.")
        return

    vectorizer = TfidfVectorizer()
    try:
        vectorizer.fit_transform([' '.join(all_index_terms)])
    except ValueError:
        print("Error during TF-IDF vectorization. Check your data.")
        return

    query_vector = vectorizer.transform([query])

    results = []

    # loop to calc similarities and append to results
    for term in query.split():
        doc_ids = get_docs(db, term)
        print(f"Term: {term}, Document IDs: {doc_ids}")

        # calc similarity for each doc
        for doc_id in doc_ids:
            terms_for_document = get_doc_terms(db, doc_id)
            print(f"Document ID: {doc_id}, Associated Terms: {terms_for_document}")
            document_vector = vectorizer.transform([' '.join(terms_for_document)])

            # to output in results
            url, name = get_url_and_name(db, doc_id)
            if url and name:
                cosine_sim = cosine_similarity(query_vector, document_vector).flatten()[0]
                results.append((url, name, cosine_sim))

    results.sort(key=lambda x: x[2], reverse=True)

    # pagination for results
    total_item_count = len(results)
    total_pages = (total_item_count + page_size - 1) // page_size

    while True:
        try:
            page_number = int(input("Enter page number or -1 to exit: "))

            if page_number == -1:
                break

            if 1 <= page_number <= total_pages:
                start_index = (page_number - 1) * page_size
                end_index = page_number * page_size
                page_data = results[start_index:end_index]
                print(f"Page: {page_number}")
                for url, name, similarity in page_data:
                    print(f"URL: {url}")
                    print(f"{name}")
                    print(f"Cosine Similarity: {similarity}")
                    print("\n")
            else:
                print("Not a valid page number. Please try again.")
                print()
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            print()

client = MongoClient()
db = client.searchengine
query = input("Search query: ")
search_engine(query, db)