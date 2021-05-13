import os

import asyncpg


DATABASE_URL = os.getenv("DATABASE_URL")

DB_POOL = asyncpg.create_pool(
    DATABASE_URL,
    min_size=1,
    max_size=2
)

IMAGE_FORMATS = ("png", "jpg", "jpeg")