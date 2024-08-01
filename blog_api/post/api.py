
from django.core.paginator import Paginator

from typing import List
from ninja import NinjaAPI

from .models import Post
from .schemas import PostResponse, PostDetailedResponse

api = NinjaAPI()

@api.get("/posts", response=List[PostResponse])
def list_posts(request, page: int = 1):
    posts = Post.objects.all().order_by('-created_at').prefetch_related('tags').only('id', 'title', 'description', 'published_at', 'tags')
    paginator = Paginator(posts, 10)
    paginated_posts = [PostResponse.from_model(post) for post in paginator.get_page(page).object_list]
    return paginated_posts

@api.get("/posts/recent", response=List[PostResponse])
def list_recent_posts(request, page: int = 1):
    posts = Post.objects.all().order_by('-created_at').only('id', 'title', 'description', 'published_at', 'tags')[:10]
    recent_posts = [PostResponse.from_model(post) for post in posts]
    return recent_posts

@api.get("/posts/tag/{tag_id}", response=List[PostResponse])
def filter_posts_by_tag(request, tag_id: int, page: int = 1):
    posts = Post.objects.filter(tags__id=tag_id).order_by('-created_at').only('id', 'title', 'description', 'published_at', 'tags')
    paginator = Paginator(posts, 10)
    paginated_posts = [PostResponse.from_model(post) for post in paginator.get_page(page).object_list]
    return paginated_posts

@api.get("/posts/{post_id}", response=PostDetailedResponse)
def get_post(request, post_id: int):
    post = Post.objects.filter(id=post_id).only('id', 'title', 'slug', 'description', 'content', 'tags', 'views', 'likes', 'created_at', 'updated_at', 'published_at').first()
    if not post:
        return {"error": "Post not found"}, 404
    
    return PostDetailedResponse.from_model(post)
