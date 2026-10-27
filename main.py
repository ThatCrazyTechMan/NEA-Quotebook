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
import starlette.status as status
import datetime


def appendToQuote(id, author, quote, date, context):
    return {
        "id": id,
        "author": author,
        "content": quote,
        "date": date,
        "context": context
    }


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
    quote = {
        "id": new_id,
        "author": author,
        "content": quote,
        "date": date,
        "context": context
    }
    quotes.append(quote)
    return RedirectResponse(
        '/quote/' + str(new_id),
        status_code=int(302)
    )


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Home"},
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


@app.get("/results/{search_term}", response_class=HTMLResponse)
async def home(request: Request, search_term: str):
    results = []
    for q in quotes:
        if search_term.lower() in q["content"].lower() or search_term.lower() in q["author"].lower():
            results.append(q)

    print(results)

    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes", "quotes": results},
    )


@app.post("/search", response_class=HTMLResponse)
async def submit(request: Request, search_term: Annotated[str, Form()]):
    print(search_term)
    return RedirectResponse(
        '/results/' + str(search_term),
        status_code=int(302)
    )
