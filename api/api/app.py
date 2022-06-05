import base64
from collections import Counter
from importlib import metadata
from pathlib import Path
from typing import List

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from .config import Settings
from .spectrogram import load_audio_bytes, plot_melspectogram

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


class Summary(BaseModel):
    url: str


@app.get("/status")
def status():
    return {"status": "ok", "version": metadata.version(__package__)}


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
async def birdclef_summary(species: str, name: str) -> Summary:
    """Return summary information about the track."""
    # TODO: the URL is hardcoded with information about the static server
    return Summary(
        url=f"{settings.static_external_host}/static"
        + f"/birdclef-2022/train_audio/{species}/{name}.ogg"
    )


@app.get("/birdclef/melspectrogram/{species}/{name}")
async def birdclef_melspectrogram(
    species: str,
    name: str,
    format="image",
    sr: int = 32000,
    n_fft=2048,
    hop_length=200,
    n_mels=16,
    mp_window=200 * 5,
    log_scaled=True,
):
    """Return an image for plotting the melspectogram of a clip."""
    summary = await birdclef_summary(species, name)
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            summary.url.replace(
                settings.static_external_host, settings.static_internal_host
            )
        )
    audio_bytes = resp.content
    y, sr = load_audio_bytes(audio_bytes, sr=sr)
    data = plot_melspectogram(y, sr, n_fft, hop_length, n_mels, mp_window, log_scaled)
    if format == "base64":
        # convert data into json response, because the node frontend has a
        # difficult serving these responses
        b64data = base64.b64encode(data).decode("utf-8")
        return {"data": f"data:image/png;base64,{b64data}"}
    else:
        return Response(data, media_type="image/png")
