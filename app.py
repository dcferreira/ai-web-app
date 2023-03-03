import os.path
from pathlib import Path
from typing import List

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from ai_web_app.main import Result, get_embeddings, index_embeddings, search

app = FastAPI()

database_path = Path("./articles.sqlite")
if os.path.exists("./saved_index"):
    embeddings = get_embeddings()
    embeddings.load("./saved_index")
else:
    logger.info("Indexing database...")
    embeddings = index_embeddings(database_path)


def get_cors_origin() -> str:
    cors_origin = os.getenv("CORS_ORIGIN")
    if cors_origin is None:
        raise ValueError(
            "`CORS_ORIGIN` environment variable not defined! "
            "Please set this to the domain from which requests "
            "to the backend will be made."
        )
    return cors_origin


origins = [
    get_cors_origin(),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search_endpoint(query: str, topn: int = 5) -> List[Result]:
    results = search(embeddings, database_path, query, topn=topn)
    return results
