from collections import Counter
from importlib import metadata
from pathlib import Path
from typing import List

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import Settings

settings = Settings()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Track(BaseModel):
    species: str
    name: str


class TrackCount(BaseModel):
    species: str
    count: int


@app.get("/version")
def version():
    return {"version": metadata.version(__package__)}


async def get_listing(host: str) -> List[Track]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{host}/static/birdclef-2022-listing.json")
    data = resp.json()

    res = []
    for item in data:
        path = Path(item)
        if path.parts[0] != "train_audio":
            continue
        _, species, name = path.parts
        res.append(Track(species=species, name=name.split(".")[0]))
    return res


@app.get("/birdclef")
async def birdclef_listing() -> List[Track]:
    return get_listing(settings.static_internal_host)


@app.get("/birdclef/species")
async def birdclef_species() -> List[TrackCount]:
    listing = await get_listing(settings.static_internal_host)
    counter = Counter([x.species for x in listing])
    return [TrackCount(species=x, count=y) for x, y in counter.items()]


@app.get("/birdclef/summary/{species}")
async def birdclef_summary_listing(species: str) -> List[Track]:
    listing = await get_listing(settings.static_internal_host)
    return [item for item in listing if item.species == species]


@app.get("/birdclef/summary/{species}/{name}")
async def birdclef_summary(species: str, name: str) -> List[Track]:
    """Return summary information about the track."""
    # TODO: the URL is hardcoded with information about the static srever
    return {
        "url": f"{settings.static_external_host}/static"
        + f"/birdclef-2022/train_audio/{species}/{name}.ogg"
    }
