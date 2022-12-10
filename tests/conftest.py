import pytest
from ankiwiktionary.wiktionary_parser import Wiktionary
from ankiwiktionary.reverso_parser import ReversoSynonyms

MOCKED_TESTS = True


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


@pytest.fixture()
def reverso_client():
    return ReversoSynonyms()
