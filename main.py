import requests
import os
import sys


def main():
    # Fetching data from Open Library API
    user_input = input("Enter ISBN or Type 'Quit': ")

    if user_input.upper() == "QUIT":
        sys.exit("Program ended.")

    book_api = f"https://openlibrary.org/isbn/{user_input}.json"
    book_response = requests.get(book_api)
    if book_response.status_code == 200:
        book_data = book_response.json()
    else:
        sys.exit("Unable to connect to OpenLibrary API.")

    try:
        author_id = book_data["authors"][0]["key"]
        author_api = f"https://openlibrary.org{author_id}.json"
        author_response = requests.get(author_api)
        author_data = author_response.json()
    except KeyError:
        sys.exit("Unable to retrieve data. Check the ISBN number.")

    # Formatting the data
    subjects_list = book_data.get("subjects", ["None"])
    subjects_str = " / ".join(subjects_list)
    subjects = subjects_str

    dewey = book_data.get("dewey_decimal_class", ["None"])

    title = book_data["title"]
    author = author_data["name"].title()

    # Posting the data to Google Sheets spreasheet
    sheety_endpoint = os.environ["ENDPOINT"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": os.environ["TOKEN"]
    }

    row_data = {
        "myBook": {
            "copies": 1,
            "title": title,
            "author": author,
            "publication": book_data["publish_date"],
            "publisher": book_data["publishers"][0],
            "isbn": user_input,
            "subjects": subjects,
            "dewey": dewey[0]
        }
    }

    sheety_response = requests.post(url=sheety_endpoint, json=row_data, headers=headers)
    if sheety_response.status_code == 200:
        print(f"'{title}' by {author} was added.")
    main()


if __name__ == "__main__":
    main()
