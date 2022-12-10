def test_synonyms(reverso_client):
    synonyms = reverso_client.get_synonyms('самый')
    assert synonyms
    assert isinstance(synonyms, list)
    for synonym in synonyms:
        assert isinstance(synonym, str)
