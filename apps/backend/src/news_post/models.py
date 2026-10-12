from sqlalchemy.orm import Mapped

from src.db import Base, created_at, deleted_at, id, updated_at


class NewsPost(Base):
    id: Mapped[id]

    author: Mapped[str]
    title: Mapped[str]
    content: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_at: Mapped[deleted_at]
