from typing import List

from ninja import NinjaAPI
from ninja.pagination import paginate, PageNumberPagination

from .models import Post
from .schemas import (
    PostResponse,
    PostDetailedResponse,
)

api = NinjaAPI()


@api.get("/posts", response=List[PostResponse])
@paginate(PageNumberPagination, page_size=10)
def list_posts(request):
    posts = (
        Post.objects.all()
        .order_by("-created_at")
        .prefetch_related("tags")
        .only("id", "title", "description", "published_at", "tags")
    )
    return [PostResponse.from_orm(post) for post in posts]


@api.get("/posts/recent", response=List[PostResponse])
def list_recent_posts(request):
    posts = (
        Post.objects.all()
        .order_by("-created_at")
        .only("id", "title", "description", "published_at", "tags")[:10]
    )
    return [PostResponse.from_orm(post) for post in posts]


@api.get("/posts/tag/{tag_id}", response=List[PostResponse])
@paginate(PageNumberPagination, page_size=10)
def filter_posts_by_tag(request, tag_id: int):
    posts = (
        Post.objects.filter(tags__id=tag_id)
        .order_by("-created_at")
        .only("id", "title", "description", "published_at", "tags")
    )
    return [PostResponse.from_orm(post) for post in posts]


@api.get("/posts/{post_id}", response=PostDetailedResponse)
def get_post(request, post_id: int):
    post = (
        Post.objects.filter(id=post_id)
        .only(
            "id",
            "title",
            "slug",
            "description",
            "content",
            "tags",
            "views",
            "likes",
            "created_at",
            "updated_at",
            "published_at",
        )
        .first()
    )
    if not post:
        return {"error": "Post not found"}, 404

    return PostDetailedResponse.from_orm(post)
