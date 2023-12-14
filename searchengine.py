from crawler import connectDataBase, Frontier, crawlerThread
from webparser import textTransformation
from query import search_engine
from pymongo import MongoClient

# Driver program for search engine
if __name__ == '__main__':

    # Initialize Database
    DB_HOST = 'localhost:27017'   
    try:
        client = MongoClient(host=[DB_HOST])
        db = client.searchengine
        pages_collection = db['pages']
        index = db['index']
        print("Connected...")
    except:
        print("Database not connected.")

    # Seed URLs for each department
    seed_urls = ['https://www.cpp.edu/cba/international-business-marketing/index.shtml']
    
    # Number of target faculty pages to find (this will be department-specific)
    num_targets = 22

    # Initialize frontier with seed URLs
    frontier = Frontier(seed_urls)

    # Start crawling
    print("Crawling web...")
    crawlerThread(frontier, num_targets, pages_collection)
    print("\n\nCrawling complete!")

    # Close the MongoDB client when done
    #client.close()

    # Parse text and insert terms into index
    textTransformation(pages_collection, index)
    print("Index creation complete!")

    print("")
    print("########## Search Engine ##############")
    print("# Type a query")
    print("# Press q to quit")

    query = ""
    while query != ("q" or "Q"):
        query = input("Enter your query: ")

        if query == ("q" or "Q"):
            print("Exiting search engine.")

        else:
            # Rank and query pages
            search_engine(query, db)