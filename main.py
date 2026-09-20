from urllib import request
import templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import jinja2

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

templates = Jinja2Templates(directory="templates")


@app.get("/quote", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "quote.html",
        {"title": "Home"},
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


@app.get("/results", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "search_results.html",
        {"title": "All quotes"},
    )
