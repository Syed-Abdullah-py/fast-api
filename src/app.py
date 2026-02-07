from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy import select
from src.schemas import PostCreate, PostResponse
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(...),
        session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy.url",
        file_type="photo",
        file_name="dummy name",
    )

    # Staging
    session.add(post)

    # Actually adding
    await session.commit()

    # Hydrating the default fields
    await session.refresh(post)

    # Return the Hydrated post object
    return post

@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Post)
        .order_by(Post.created_at.desc())
    )

    return result.scalars().all()