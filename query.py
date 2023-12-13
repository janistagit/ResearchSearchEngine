from crawler import connectDataBase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

page_size = 5

# Connect to MongoDB
client = MongoClient()
db = client.business_department
pages = db.Professor_information

def search_faculty(query, faculty_data):
    faculty_info = []

    for faculty in faculty_data:
        curr = f"{faculty.get('Name', '')} {faculty.get('Title', '')} {faculty.get('About', '')} {faculty.get('Publications', '')} {faculty.get('Student Projects', '')} {faculty.get('Affiliations', '')} {faculty.get('Research Interests', '')} {faculty.get('IBM Courses Taught', '')} {faculty.get('Education', '')}"
        faculty_info.append(curr)

    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    query_matrix = tfidfvectorizer.fit_transform([query])
    faculty_matrix = tfidfvectorizer.transform(faculty_info)
    cos_sim = cosine_similarity(query_matrix, faculty_matrix).flatten()
    #print(cos_sim)

    # sort by cosine similarity and create list of resulting pages
    faculty_ranking = sorted(list(enumerate(cos_sim)), key=lambda x: x[1], reverse=True)
    results = []
    for i, similarity in faculty_ranking:
        prof_info = faculty_data[i]
        prof_info['cos_sim'] = similarity
        results.append(prof_info)

    return results


def pagination(results, page_size):
    total_item_count = len(results)
    total_pages = (total_item_count + page_size - 1) // page_size

    while True:
        try:
            page_number = int(input("Enter page number: "))
            if 1 <= page_number <= total_pages:
                start_index = (page_number - 1) * page_size
                end_index = page_number * page_size
                page_data = results[start_index:end_index]
                for result in page_data:
                    print(f"Cosine similarity: {result['cos_sim']}")
                    print(f"Professor: {result['Name']}")
                    print(f"Title: {result['Title']}")
                    print(f"Email: {result['Email:']}")
                    print(f"Phone: {result['Phone']}")
                    print(f"Office: {result['Office']}")
                    print("\n")
            else:
                print("Not a valid page number. Please try again.")
                print()
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            print()


# search query and info
query = "sales force"
db_data = list(pages.find())
results = search_faculty(query, db_data)

pagination(results, page_size)


#commented out just in case
'''
for result in results:
    print(f"Cosine similarity: {result['cos_sim']}")
    print(f"Professor: {result['Name']}")
    print(f"Title: {result['Title']}")
    print(f"Email: {result['Email:']}")
    print(f"Phone: {result['Phone']}")
    print(f"Office: {result['Office']}")
    print("\n")
'''