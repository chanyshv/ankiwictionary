import pytest
from ankiwictionary.parser import Wictionary


@pytest.fixture()
def client():
    return Wictionary()


@pytest.fixture(params=['палка', 'привет', 'футболка'])
def word(request):
    return request.param
