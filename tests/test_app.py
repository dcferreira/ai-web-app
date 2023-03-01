import pytest
import requests
from xprocess import ProcessStarter


class TestPythonServer:
    @pytest.fixture(scope="module")
    def server(self, xprocess):
        class Starter(ProcessStarter):
            timeout = 600
            pattern = "Application startup complete"
            args = ["hatch", "run", "serve"]

        xprocess.ensure("server", Starter)
        url = "http://127.0.0.1:8080"
        yield url

        xprocess.getinfo("server").terminate()

    @pytest.mark.integration
    def test_valid_search(self, server):
        topn = 5
        response = requests.get(
            server + "/search", params={"query": "symptoms of covid", "topn": topn}
        )

        assert response.status_code == 200
        assert len(response.json()) == topn

    @pytest.mark.integration
    def test_empty_search(self, server):
        response = requests.get(server + "/search")

        assert response.status_code == 422
