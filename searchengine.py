from crawler import *
from webparser import *
from query import *

# Driver program for search engine
if __name__ == '__main__':

    # Initialize Database
    db, client = connectDataBase()
    pages_collection = db.pages

    # Seed URLs for each department
    seed_urls = ['https://www.cpp.edu/cba/international-business-marketing/index.shtml']
    
    # Number of target faculty pages to find (this will be department-specific)
    num_targets = 22

    # Initialize frontier with seed URLs
    frontier = Frontier(seed_urls)

    # Start crawling
    crawlerThread(frontier, num_targets)
    print("\n\nCrawling complete!")

    # Close the MongoDB client when done
    #client.close()

    # Parse text and insert terms into index
    textTransformation()
    print("Index creation complete!")

    print("")
    print("########## Search Engine ##############")
    print("# Type a query")
    print("# Press q to quit")

    query = ""
    while query != ("q" | "Q"):
        query = input("Enter your query: ")

        if query == ("q" | "Q"):
            print("Exiting search engine.")

        else:
            # Rank and query pages
            search_engine(query, db)