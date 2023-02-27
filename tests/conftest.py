import sqlite3
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import pytest


@pytest.fixture(scope="module")
def assets_path():
    return Path(__file__).resolve().parent / "assets"


@pytest.fixture(scope="module")
def articles_database(assets_path) -> Path:
    with NamedTemporaryFile() as f:
        conn = sqlite3.connect(f.name)

        # load CSVs
        articles = pd.read_csv(assets_path / "articles.csv", sep=",")
        sections = pd.read_csv(assets_path / "sections.csv", sep=",")

        # write CSVs to DB
        articles.to_sql("articles", conn, index=False)
        sections.to_sql("sections", conn, index=False)

        yield Path(f.name)
