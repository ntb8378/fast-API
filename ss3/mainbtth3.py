from fastapi import FastAPI
app = FastAPI()
books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_avaliable": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_avaliable": True
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_avaliable": False
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_avaliable": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_avaliable": True
    }
]

@app.get("/books/statistics")
def count_statistics():
    count_book = 0
    book_true = 0
    book_false = 0
    for book in books:
        count_book += 1
        if book["is_avaliable"] == True:
            book_true += 1
        else:
            book_false += 1

    return {

  "total_books": {count_book},

  "available_books": {book_true},

  "borrowed_books": {book_false}

}

@app.get("/books/categories")
def categories_book():
    categories = []

    for book in books:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {
        "categories": categories
    }

# cách dùng set
# @app.get("/books/categories")
# def categories_book():
#     categories = set()

#     for book in books:
#         categories.add(book["category"])

#     return {
#         "categories": list(categories)
#     }


@app.get("/books/latest")
def latest_book():
    if len(books) == 0:
        return {
            "message": "No books available"
        }

    latest_book = books[0]

    for book in books:
        if book["year"] > latest_book["year"]:
            latest_book = book

    return latest_book