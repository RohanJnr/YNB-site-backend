from typing import Optional

from pydantic import BaseModel


class MinecraftImage(BaseModel):
    image_description: Optional[str] = None
    url: str


class Tag:
    tag_type: str


class CategoryData:
    tag_type: str
    title: Optional[str] = None
    info: str
