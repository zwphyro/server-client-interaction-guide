from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.news_post.models import NewsPost


class NewsPostRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self):
        query = select(NewsPost).where(NewsPost.deleted_at.is_(None))
        result = await self._session.execute(query)

        return result.scalars().all()

    async def get_by_id(self, id: str):
        query = select(NewsPost).where(NewsPost.id == id, NewsPost.deleted_at.is_(None))
        result = await self._session.execute(query)

        return result.scalars().first()

    async def create(self, author: str, title: str, content: str):
        post = NewsPost(author=author, title=title, content=content)
        self._session.add(post)

        return post

    async def update_by_id(self, id: str, **values):
        query = (
            update(NewsPost)
            .where(NewsPost.id == id, NewsPost.deleted_at.is_(None))
            .values(**values)
            .returning(NewsPost)
        )
        result = await self._session.execute(query)

        return result.scalars().first()

    async def delete_by_id(self, id: str):
        return await self.update_by_id(id, deleted_at=func.now())
