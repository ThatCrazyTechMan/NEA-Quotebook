import json
import random
from datetime import date
from pathlib import Path

import templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated
from urllib.parse import quote
import random
import starlette.status as status
import datetime


def appendToQuote(quote_list, id, author, quote, date, context):
    quote_list.append(
        {
            "id": id,
            "author": author,
            "content": quote,
            "date": date,
            "context": context
        }
    )


# def quoteExists(quotelist, author, quote, date, context):
# if quotelist["author"] == author and quotelist["quote"] == quote and quotelist["date"] == date and quotelist[
#   "context"] == context:
#    return True
# else:
#    return False


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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
async def home(request: Request, quote_id: int):
    quote = None
    for q in quotes:
        if q["id"] == quote_id:
            quote = q
            break

    related = []
    for q in quotes:
        if q["author"] == quote["author"] and q["id"] != quote["id"]:
            related.append(q)
    return templates.TemplateResponse(
        request,
        "quote.html",
        {"title": "quote", "quote": quote, "related": related},
    )


@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, author: Annotated[str, Form()], quote: Annotated[str, Form()],
                 context: Annotated[str, Form()],
                 date: Annotated[str, Form()]):
    ids = []
    for q in quotes:
        ids.append(q["id"])

    new_id = int(max(ids) + 1)
    appendToQuote(quotes, new_id, author, quote, date, context)
    return RedirectResponse(
        '/quote/' + str(new_id),
        status_code=int(302)
    )


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    rand_quote = random.choice(quotes)
    person_of_month = random.choice(quotes)["author"]
    quotes_from_pom = []
    counter = 0
    for q in quotes:
        if q["author"] == person_of_month and counter < 4:
            quotes_from_pom.append(q)
            counter += 1

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
    return templates.TemplateResponse(
        request,
        "login.html",
        {"title": "Login"},
    )


@app.get("/results/{search}", response_class=HTMLResponse)
async def home(request: Request, search: str):
    results = []
    for q in quotes:
        if search.lower() in q["content"].lower() or search.lower() in q["author"].lower():
            results.append(q)

    print(results)

    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes", "quotes": results},
    )


@app.post("/search", response_class=HTMLResponse)
async def submit(request: Request, search: Annotated[str, Form()]):
    print(search)
    return RedirectResponse(
        '/results/' + quote(search.strip(), safe=""),
        status_code=int(302)
    )


@app.get("/quote-exists", response_class=HTMLResponse)
async def exists(request: Request):
    return templates.TemplateResponse(
        request,
        "quote_exists.html",
        {"title": "Quote Exists"},
    )
