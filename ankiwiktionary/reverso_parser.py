import dataclasses

import yarl
import requests
import lxml.html


@dataclasses.dataclass()
class Synonym:
    word: str
    example: str


class ReversoSynonyms:
    _SEARCH_URL = "https://synonyms.reverso.net/синонимы/ru/"
    _USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    @classmethod
    def get_synonyms(cls, word: str):
        url = yarl.URL(cls._SEARCH_URL) / word
        headers = {
            'User-Agent': cls._USER_AGENT
        }
        r = requests.get(str(url), headers=headers)
        r.raise_for_status()
        parsed_page = lxml.html.fromstring(r.text)
        raw_synonyms = parsed_page.xpath('//a[@class="synonym  relevant"]')
        synonyms = [i.text for i in raw_synonyms]
        return synonyms
