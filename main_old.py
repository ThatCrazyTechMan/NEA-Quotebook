import json
import random
from datetime import date
from pathlib import Path

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

import templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated, Any, Sequence
from urllib.parse import quote
import databaseConnector
from sqlalchemy import text, Row
import hashlib
from starlette.middleware.sessions import SessionMiddleware


async def getQuoteFromAuthor(author):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE author = :author"
    stmt = text(sql_query)
    POM_quotes_results = session.execute(stmt, {"author": author})
    quotes_from_pom = POM_quotes_results.all()
    return quotes_from_pom


async def getRandomAuthor():
    session = databaseConnector.get_session()
    sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    POM_result = session.execute(stmt)
    person_of_month = POM_result.first().author
    return person_of_month


async def getRandomQuote():
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    rand_quote_result = session.execute(stmt)
    rand_quote = rand_quote_result.first()
    return rand_quote

def appendToQuote(author, quote, date, context, username):
    session = databaseConnector.get_session()
    sql_query = "INSERT INTO quote(author, content, date, context, username) VALUES(:author, :content, :date, :context, :username) RETURNING id"
    stmt = text(sql_query)
    result = session.execute(stmt, {"author": author, "content": quote, "date": date, "context": context, "username": username  })
    new_id=result.scalar_one()
    session.commit()

    return new_id

def quoteExists(content, author):
       session = databaseConnector.get_session()
       sql_query = "SELECT COUNT(*) FROM quote WHERE content = :content AND author = :author"
       stmt = text(sql_query)
       result = session.execute(stmt, {"author": author, "content": content})
       result = result.scalar_one()
       session.commit()
       print(result)
       if result != 0:
           return True
       else:
           return False


def searchQuotes(search):
    session = databaseConnector.get_session()
    search = f"%{search}%"
    sql_query = "SELECT * FROM quote WHERE content ILIKE :search OR author ILIKE :search"
    stmt = text(sql_query)
    result = session.execute(stmt, {"search": search})
    session.commit()
    return result.all()

def getRelated(quote):
    session = databaseConnector.get_session()
    sql_query = "SELECT content FROM quote WHERE author = :author AND id <> :id"
    stmt = text(sql_query)
    relateds_result = session.execute(stmt, {"author": quote.author, "id": quote.id})
    relateds = relateds_result.all()
    return relateds


def getQuote(quote_id):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE id = :id"
    stmt = text(sql_query)
    db_result = session.execute(stmt, {"id": quote_id})
    quote = db_result.first()
    return quote

async def getQuoteFromAuthor(author):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE author = :author"
    stmt = text(sql_query)
    POM_quotes_results = session.execute(stmt, {"author": author})
    quotes_from_pom = POM_quotes_results.all()
    return quotes_from_pom


async def getRandomAuthor():
    session = databaseConnector.get_session()
    sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    POM_result = session.execute(stmt)
    person_of_month = POM_result.first().author
    return person_of_month


async def getRandomQuote():
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    rand_quote_result = session.execute(stmt)
    rand_quote = rand_quote_result.first()
    return rand_quote
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    SessionMiddleware,
    secret_key="secret"
)


templates = Jinja2Templates(directory="templates")




quotes = [
    {
        "id": 1,
        "author": "Kabir Marathe",
        "content": "You have to start in the trenches to appreciate the penthouse",
        "date": "02/04/2025",
        "context": "Said on the first week of school"
    },
    {
        "id": 2,
        "author": "Lilly Jesse",
        "content": "I don't know how long it takes by road, I have only been there by tractor",
        "date": "17/05/2025",
        "context": "Didn't know how to go to her local pub by car"
    },
    {
        "id": 3,
        "author": "Mathew Gilbert",
        "content": "Super mega gay. Like James Charles but half as cute and twice as gay",
        "date": "22/08/2025",
        "context": "His tragic story about how a crying girl who had just broke up with her boyfriend tried hitting on him and he panicked "
    },
    {
        "id": 4,
        "author": "Sonny Thurner",
        "content": "You're schizophrenic, I'm gay",
        "date": "24/01/2026",
        "context": "God alone knows"
    },
    {
        "id": 5,
        "author": "Mathew Gilbert",
        "content": "I have never had watermelon before",
        "date": "01/07/2026",
        "context": "Mat Gilbert on how many foods he has never tried, and he is the 'adventurous' member of his family"
    },
    {
        "id": 6,
        "author": "Louie Allerton",
        "content": "Who is Josh Hall?",
        "date": "16/09/2026",
        "context": "Josh Hall was directly behind him at time of quoting"
    }
]


@app.get("/quote/{quote_id}", response_class=HTMLResponse)
def quote(request: Request, quote_id: int):
    quote = getQuote(quote_id)
    relateds = getRelated(quote)

    return templates.TemplateResponse(
        request,
        "quote.html",
        {"title": "quote", "quote": quote, "related": relateds},
    )


@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, author: Annotated[str, Form()], quote: Annotated[str, Form()],
                 context: Annotated[str, Form()],
                 date: Annotated[str, Form()]):


    if not quoteExists(quote, author):
        username = request.session["username"]
        print(username)
        new_id = appendToQuote(author, quote, date, context, username)
        return RedirectResponse(
            '/quote/' + str(new_id),
            status_code=int(302)
        )
    else:
        return templates.TemplateResponse(
            request,
            "quote_exists.html",
            {"title": "Quote Exists"}
        )


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    rand_quote = await getRandomQuote()

    person_of_month = await getRandomAuthor()

    quotes_from_pom = await getQuoteFromAuthor(person_of_month)

    print(rand_quote)
    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Home", "rand": rand_quote, "person_of_month": person_of_month, "POM_quotes": quotes_from_pom},
    )
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"title": "index"},
    )


@app.get("/login", response_class=HTMLResponse)
async def home(request: Request):
    rand_quote = await getRandomQuote()
    print(rand_quote)
    return templates.TemplateResponse(
        request,
        "login.html",
        {"title": "Login", "rand_quote": rand_quote},
    )

@app.post("/user", response_class=HTMLResponse)
async def user(request: Request, username: Annotated[str, Form()]):
    print(f"{username} tried logging in!!")
    session = databaseConnector.get_session()
    sql_query = "SELECT COUNT(*) FROM users WHERE username = :username"
    stmt = text(sql_query)
    user_result = session.execute(stmt, {"username": username})
    user_count = user_result.scalar_one()

    if user_count == 0:
        return templates.TemplateResponse(
            request,
            "signup.html",
            {"title": "Create", "username": username},
        )
    else:
        return templates.TemplateResponse(
            request,
            "signin.html",
            {"title": "Login", "username": username},
        )

@app.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM users WHERE username = :username AND :password_hash = password_hash"
    stmt = text(sql_query)
    signin_result = session.execute(stmt, {"username": username, "password_hash": password_hash})
    user = signin_result.first()
    print(user)
    if user is not None:
        print(f"{username} logged in!!")
        request.session["username"] = username
        return RedirectResponse(
            '/home',
            status_code=int(302)
        )
    else:
        return templates.TemplateResponse(
            request,
            "signin.html",
            {"title": "Login", "username": username},
        )

@app.post("/signup", response_class=HTMLResponse)
async def signin(request: Request, username: Annotated[str, Form()], password1: Annotated[str, Form()], password2: Annotated[str, Form()]):
    if password1 != password2:
        return templates.TemplateResponse(
            request,
            "signup.html",
            {"title": "Signup", "username": username}
        )
    else:
        password_hash = hashlib.sha256(password1.encode()).hexdigest()
        session = databaseConnector.get_session()
        sql_query = "INSERT INTO users(username, password_hash) VALUES (:username, :password_hash)"
        stmt = text(sql_query)
        session.execute(stmt, {"username": username, "password_hash": password_hash})
        session.commit()
        print(f"{username} created!!")
        return RedirectResponse(
            '/login',
            status_code=int(302)

        )




@app.get("/results/{search}", response_class=HTMLResponse)
async def home(request: Request, search: str):
    results = searchQuotes(search)
    print(results)

    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes", "quotes": results},
    )


@app.post("/search", response_class=HTMLResponse)
async def submit(request: Request, search: Annotated[str, Form()]):
    print(search)
    quotes = searchQuotes(search)
    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes", "quotes": quotes},
    )


@app.get("/quote-exists", response_class=HTMLResponse)
async def exists(request: Request):
    return templates.TemplateResponse(
        request,
        "quote_exists.html",
        {"title": "Quote Exists"},
    )