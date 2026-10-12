from fastapi import APIRouter

from src.news_post.routes import router as news_posts_router

router = APIRouter()
router.include_router(news_posts_router, prefix="/news-posts", tags=["News Posts"])
