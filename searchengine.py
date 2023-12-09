from crawler import *
from webparser import *
from query import *

# Driver program for search engine
if __name__ == '__main__':
    db = connectDataBase()

    print("")
    print("########## Search Engine ##############")
    print("#Type a query")
    print("#Press q to quit")

    query = ""
    while query != ("q" | "Q"):
        query = input("Enter your query: ")

        if query == ("q" | "Q"):
            print("Exiting search engine.")

        else:
            # Insert search engine functions
            pass