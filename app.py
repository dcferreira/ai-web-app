from pathlib import Path
from typing import List

from fastapi import FastAPI
from loguru import logger

from ai_web_app.main import Result, index_embeddings, search

app = FastAPI()

logger.info("Indexing database...")
database_path = Path("./articles.sqlite")
embeddings = index_embeddings(database_path)


@app.get("/search")
async def search_endpoint(query: str, topn: int = 5) -> List[Result]:
    results = search(embeddings, database_path, query, topn=topn)
    return results
