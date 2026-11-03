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
import functions

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    SessionMiddleware,
    secret_key="secret"
)


templates = Jinja2Templates(directory="templates")

@app.get("/quote/{quote_id}", response_class=HTMLResponse)
def quote(request: Request, quote_id: int):
    quote = functions.getQuote(quote_id)
    relateds = functions.getRelated(quote)

    return templates.TemplateResponse(
        request,
        "quote.html",
        {"title": "quote", "quote": quote, "related": relateds},
    )


@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, author: Annotated[str, Form()], quote: Annotated[str, Form()],
                 context: Annotated[str, Form()],
                 date: Annotated[str, Form()]):


    if not functions.quoteExists(quote, author):
        user_id = request.session["user_id"]
        print(user_id)
        new_id = functions.appendToQuote(author, quote, date, context, user_id)
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
    rand_quote = await functions.getRandomQuote()

    person_of_month = await functions.getRandomAuthor()

    quotes_from_pom = await functions.getQuoteFromAuthor(person_of_month)


    print(rand_quote)
    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Home", "rand": rand_quote, "person_of_month": person_of_month, "POM_quotes": quotes_from_pom, "username": str(functions.getUsernameFromID(user_id = request.session["user_id"]))},
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
    rand_quote = await functions.getRandomQuote()
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
        request.session["user_id"] = str(functions.getUser_IDFromUsername(username))
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
    results = functions.searchQuotes(search)
    print(results)

    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes", "quotes": results},
    )


@app.post("/search", response_class=HTMLResponse)
async def submit(request: Request, search: Annotated[str, Form()]):
    print(search)
    quotes = functions.searchQuotes(search)
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