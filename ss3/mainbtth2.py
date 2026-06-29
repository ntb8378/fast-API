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

@app.get("/books/available")
def check_health():
    avalible_book = []
    for book in books:
        if book["is_avaliable"] == True:
            avalible_book.append(book)

    return avalible_book


@app.get("/books/borrowed")
def check_health_false():
    avalible_book_false = []
    for book in books:
        if book["is_avaliable"] == False:
            avalible_book_false.append(book)

    return avalible_book_false
