import typing as ty

import vcr

from ankiwiktionary.parser import Word, Meaning


@vcr.use_cassette('tests/vcr_cassetes/word.yaml')
def test_get_word(client, word):
    parsed = client.get_word(word)
    assert parsed
    assert isinstance(parsed, Word)
    assert isinstance(parsed.meanings, ty.Sequence)
    for m in parsed.meanings:
        assert isinstance(m, Meaning)
        if m.examples:
            for ex in m.examples:
                assert isinstance(ex, str)
        assert m.definition
    assert parsed.word == word


@vcr.use_cassette('tests/vcr_cassetes/search.yaml')
def test_search(client, word):
    search_results = client.search(word)
    assert search_results
    assert isinstance(search_results, ty.Sequence)
    for res in search_results:
        assert isinstance(res, str)
