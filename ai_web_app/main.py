import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import regex as re
from loguru import logger
from txtai.embeddings import Embeddings
from txtai.pipeline import Tokenizer


def index_embeddings(database: Path) -> Embeddings:
    def stream():
        # Connection to database file
        db = sqlite3.connect(database)
        cur = db.cursor()

        # Select tagged sentences without a NLP label.
        # NLP labels are set for non-informative sentences.
        cur.execute(
            "SELECT Id, Name, Text FROM sections "
            "WHERE (labels is null or labels NOT IN ('FRAGMENT', 'QUESTION')) "
            "AND tags is not null"
        )

        count = 0
        for row in cur:
            # Unpack row
            uid, name, text = row

            # Only process certain document sections
            if not name or not re.search(
                r"background|(?<!.*?results.*?)discussion|introduction|reference",
                name.lower(),
            ):
                # Tokenize text
                tokens = Tokenizer.tokenize(text)

                document = (uid, tokens, None)

                count += 1
                if count % 1000 == 0:
                    logger.debug(f"Streamed {count} documents")

                # Skip documents with no tokens parsed
                if tokens:
                    yield document

        logger.info(f"Iterated over {count} total rows")

        # Free database resources
        db.close()

    # BM25 + fastText vectors
    embeddings = Embeddings(
        {
            "method": "sentence-transformers",
            "path": "all-MiniLM-L6-v2",
            "scoring": "bm25",
        }
    )

    embeddings.index(stream())

    return embeddings


@dataclass
class Result:
    id: str
    title: str
    published: datetime
    reference: str
    text: str
    score: float


def search(
    embeddings: Embeddings, database: Path, query: str, topn: int = 5
) -> List[Result]:
    db = sqlite3.connect(database)
    cur = db.cursor()

    results: List[Result] = []
    for uid, score in embeddings.search(query, topn):
        cur.execute("SELECT article, text FROM sections WHERE id = ?", [uid])
        uid, text = cur.fetchone()

        cur.execute(
            "SELECT Title, Published, Reference from articles where id = ?", [uid]
        )
        res = cur.fetchone()
        results.append(
            Result(
                id=uid,
                title=res[0],
                published=res[1],
                reference=res[2],
                text=text,
                score=score,
            )
        )

    db.close()
    return results
