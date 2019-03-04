import pytest
from api import api


@pytest.fixture
def app():
    return api.app
