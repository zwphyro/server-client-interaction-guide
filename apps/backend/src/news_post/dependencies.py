from typing import Annotated

from fastapi import Depends

from src.dependencies import UOWDependency
from src.news_post.service import NewsPostService


def get_news_post_service(
    uow: UOWDependency,
):
    return NewsPostService(uow)


ServiceDependency = Annotated[NewsPostService, Depends(get_news_post_service)]
