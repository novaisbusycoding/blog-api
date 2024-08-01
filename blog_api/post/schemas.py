from typing import List
from ninja import Schema

class TagResponse(Schema):
    name: str
    id: int

class PostResponse(Schema):
    id: int
    title: str
    slug: str
    description: str
    published_at: str
    tags: List[TagResponse] 

    @classmethod
    def from_model(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            slug=post.slug,
            description=post.description,
            tags=[TagResponse(id=tag.id, name=tag.name) for tag in post.tags.all()],
            published_at=post.published_at.isoformat() if post.published_at else None,
        )

class PostDetailedResponse(Schema):
    id: int
    title: str
    slug: str
    description: str
    content: str 
    tags: List[int]
    views: int = 0
    likes: int = 0
    created_at: str
    updated_at: str
    published_at: str
    tags: List[TagResponse]

    @classmethod
    def from_model(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            slug=post.slug,
            description=post.description,
            content=post.content,
            tags=[TagResponse(id=tag.id, name=tag.name) for tag in post.tags.all()],
            views=post.views,
            likes=post.likes,
            created_at=post.created_at.isoformat() if post.created_at else None,
            updated_at=post.updated_at.isoformat() if post.updated_at else None,
            published_at=post.published_at.isoformat() if post.published_at else None,
        )