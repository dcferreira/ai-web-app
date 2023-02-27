from pathlib import Path

from txtai.embeddings import Embeddings


def index_embeddings(database: Path) -> Embeddings:
    raise NotImplementedError


def search(embeddings: Embeddings, database: Path, query: str, topn: int = 5):
    raise NotImplementedError
