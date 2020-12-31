import dataclasses
import typing as ty

import requests as rq
import yarl
from lxml import etree, html


@dataclasses.dataclass()
class Meaning:
    definition: str
    examples: ty.Sequence[str]


@dataclasses.dataclass()
class Word:
    meanings: ty.Sequence[Meaning]
    word: str


class Wictionary:
    _WORD_URL = 'https://ru.wiktionary.org/wiki/'

    def __init__(self):
        self._session = rq.Session()

    def _get_page(self, word) -> etree._Element:
        url = yarl.URL(self._WORD_URL) / word
        r = self._session.get(str(url))
        parsed_page: etree._Element = html.fromstring(r.text)
        return parsed_page

    def get_word(self, word: str):
        page = self._get_page(word)
        raw_meanings = page.xpath('//div[@id="mw-content-text"]/div[@class="mw-parser-output"]/ol[1]/li[not(@class)]')
        meanings = []
        for m in raw_meanings:
            meanings.append(self._parse_meaning(m))
        return Word(meanings, word)

    def _parse_definition(self, elm: etree._Element):
        t = elm.text
        if t:
            yield t
        for e in elm:
            if e.tag == 'span' and e.attrib.get('class') == 'example-details':
                continue
            e: etree._Element
            yield from e.itertext()
            t = e.tail
            if t:
                yield t

    def _parse_example(self, elm: etree._Element):
        t = elm.text
        if t:
            yield t
        for e in elm:
            if e.tag == 'span' and e.attrib.get('class') == 'example-details':
                continue
            e: etree._Element
            yield from e.itertext()
            t = e.tail
            if t:
                yield t

    def _parse_meaning(self, elm: etree._Element) -> Meaning:
        definition = ''.join(self._parse_definition(elm))
        raw_examples = elm.xpath('./span[@class="example-fullblock"]/span[@class="example-block"]')
        parsed_examples = []
        for e in raw_examples:
            example = ''.join(self._parse_example(e))
            parsed_examples.append(example)
        return Meaning(definition, parsed_examples)
