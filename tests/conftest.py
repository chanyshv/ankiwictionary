import pytest
from ankiwiktionary.parser import Wiktionary

MOCKED_TESTS = True


# MOCKED_TESTS = False


@pytest.fixture()
def client():
    return Wiktionary()


def _get_word_parameters():
    words = ['самый', 'темный', 'час', 'это', 'час', 'перед', 'рассветом']
    if not MOCKED_TESTS:
        return words
    return [words[0]]


@pytest.fixture(params=_get_word_parameters())
def word(request):
    return request.param
