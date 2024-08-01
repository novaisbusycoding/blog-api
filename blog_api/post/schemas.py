from datetime import datetime
from typing import List
from ninja import Schema


class TagResponse(Schema):
    id: int
    name: str


class PostResponse(Schema):
    id: int
    title: str
    slug: str
    description: str
    published_at: datetime
    tags: List[TagResponse]


class PostDetailedResponse(Schema):
    id: int
    title: str
    slug: str
    description: str
    content: str
    tags: List[int]
    views: int = 0
    likes: int = 0
    created_at: datetime
    updated_at: datetime
    published_at: datetime
    tags: List[TagResponse]
