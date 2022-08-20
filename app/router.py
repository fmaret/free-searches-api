from fastapi import APIRouter
from app.google_search import make_google_search


route = APIRouter()


@route.get("/google-search")
def google_search(search):
    return make_google_search(search)