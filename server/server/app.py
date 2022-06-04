from importlib import metadata

from fastapi import FastAPI

app = FastAPI()


@app.get("/version")
def read_root():
    return {"version": metadata.version(__package__)}
