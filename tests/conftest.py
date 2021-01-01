import pytest
from ankiwictionary.parser import Wictionary

MOCKED_TESTS = True


# MOCKED_TESTS = False


@pytest.fixture()
def client():
    return Wictionary()


def _get_word_parameters():
    words = ['самый', 'темный', 'час', 'это', 'час', 'перед', 'рассветом']
    if not MOCKED_TESTS:
        return words
    return [words[0]]


@pytest.fixture(params=_get_word_parameters())
def word(request):
    return request.param
