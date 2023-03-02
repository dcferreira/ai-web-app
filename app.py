import os.path
from pathlib import Path
from typing import List

from fastapi import FastAPI
from loguru import logger

from ai_web_app.main import Result, get_embeddings, index_embeddings, search

app = FastAPI()

database_path = Path("./articles.sqlite")
if os.path.exists("./saved_index"):
    embeddings = get_embeddings()
    embeddings.load("./saved_index")
else:
    logger.info("Indexing database...")
    embeddings = index_embeddings(database_path)


@app.get("/search")
async def search_endpoint(query: str, topn: int = 5) -> List[Result]:
    results = search(embeddings, database_path, query, topn=topn)
    return results
