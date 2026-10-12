import logging

from src.exceptions import NotFoundError
from src.uow import UnitOfWork

log = logging.getLogger(__name__)


class NewsPostService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self._uow = uow

    async def create_news_post(self, *, author: str, title: str, content: str):
        news_post = await self._uow.news_post.create(author, title, content)

        await self._uow.commit()
        return news_post

    async def get_news_post(self, id: str):
        news_post = await self._uow.news_post.get_by_id(id)
        if news_post is None:
            raise NotFoundError

        return news_post

    async def list_news_posts(self):
        return await self._uow.news_post.list()

    async def replace_news_post(
        self, id: str, *, author: str, title: str, content: str
    ):
        return await self.update_news_post(
            id, author=author, title=title, content=content
        )

    async def update_news_post(self, id: str, **values):
        if not values:
            return await self.get_news_post(id)

        news_post = await self._uow.news_post.update_by_id(id, **values)
        if news_post is None:
            raise NotFoundError

        await self._uow.commit()
        return news_post

    async def delete_news_post(self, id: str):
        news_post = await self._uow.news_post.delete_by_id(id)
        if news_post is None:
            raise NotFoundError

        await self._uow.commit()
        return news_post
