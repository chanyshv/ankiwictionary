import pytest
from ankigen.parser import Wictionary


@pytest.fixture()
def client():
    return Wictionary()


@pytest.fixture(params=['палка'])
def word(request):
    return request.param
