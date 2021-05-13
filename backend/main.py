from typing import Callable

import httpx
from asyncpg import Connection
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from backend import constants
from backend.models import MinecraftImage


app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    await constants.DB_POOL


@app.middleware("http")
async def attach_db_conn(request: Request, call_next: Callable) -> Response:
    async with constants.DB_POOL.acquire() as conn:
        request.state.database_connection = conn
        response = await call_next(request)
    return response


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Close down the app."""
    await constants.DB_POOL.close()


@app.get("/")
async def home(request: Request) -> dict:
    return {"message": "Home page"}


async def verify_image_url(url: str) -> None:
    """Verify if url is True and is an image."""
    if url.endswith(constants.IMAGE_FORMATS):
        return

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except Exception as e:
            if isinstance(e, (httpx.InvalidURL, httpx.HTTPStatusError, httpx.UnsupportedProtocol)):
                raise HTTPException(status_code=400, detail="Invalid URL.")
            # Log error
            raise e


@app.post("/minecraft_images")
async def minecraft_images(request: Request, image: MinecraftImage) -> dict:
    """Add minecraft image to database."""
    await verify_image_url(image.url)

    # `Connection` type hint for code intellisense/auto complete.
    connection: Connection = request.state.database_connection
    async with connection.transaction():
        await connection.execute(
            "INSERT INTO minecraft_images VALUES ($1, $2);",
            image.image_description,
            image.url
        )
    
    return image
