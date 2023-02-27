import pytest

from ai_web_app.main import index_embeddings, search


@pytest.fixture
def example_embeddings(articles_database):
    return index_embeddings(articles_database)


def test_index_embeddings_count(example_embeddings):
    assert example_embeddings.count() == 2


def test_search(example_embeddings, articles_database):
    res_sports = search(example_embeddings, articles_database, "sports", 1)
    assert res_sports[0].id == "08as6hga"

    res_military = search(example_embeddings, articles_database, "army", 1)
    assert res_military[0].id == "071hvhme"
