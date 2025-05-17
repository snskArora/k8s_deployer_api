from fastapi import FastAPI

app = FastAPI()
serve = app.get


@serve('/')
def index():
    return {"server": "started"}
