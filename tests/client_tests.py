def test_get_word(client, word):
    parsed = client.get_word('роботыва')
    assert parsed
