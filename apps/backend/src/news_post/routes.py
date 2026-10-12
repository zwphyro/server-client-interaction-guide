from fastapi import APIRouter, status

from src.news_post.dependencies import ServiceDependency
from src.news_post.schemas import (
    CreateNewsPostRequest,
    NewsPostSchema,
    UpdateNewsPostRequest,
)
from src.schemas import HTTPExceptionSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NewsPostSchema)
async def create_news_post(
    new_news_post: CreateNewsPostRequest,
    service: ServiceDependency,
):
    return await service.create_news_post(
        author=new_news_post.author,
        title=new_news_post.title,
        content=new_news_post.content,
    )


@router.get(
    "/{id}",
    response_model=NewsPostSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def get_news_post(id: str, service: ServiceDependency):
    return await service.get_news_post(id)


@router.get("/", response_model=list[NewsPostSchema])
async def list_news_posts(service: ServiceDependency):
    return await service.list_news_posts()


@router.put(
    "/{id}",
    response_model=NewsPostSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def replace_news_post(
    id: str,
    new_news_post: CreateNewsPostRequest,
    service: ServiceDependency,
):
    return await service.replace_news_post(
        id,
        author=new_news_post.author,
        title=new_news_post.title,
        content=new_news_post.content,
    )


@router.patch(
    "/{id}",
    response_model=NewsPostSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def update_news_post(
    id: str, new_news_post: UpdateNewsPostRequest, service: ServiceDependency
):
    return await service.update_news_post(
        id, **new_news_post.model_dump(exclude_unset=True)
    )


@router.delete(
    "/{id}",
    response_model=NewsPostSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def delete_news_post(id: str, service: ServiceDependency):
    return await service.delete_news_post(id)
