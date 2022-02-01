from typing import Generator

import pytest
from fastapi.testclient import TestClient

from pantapalabras.api import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
