def test_get_word(client, word):
    parsed = client.get_word('робот')
    assert parsed
