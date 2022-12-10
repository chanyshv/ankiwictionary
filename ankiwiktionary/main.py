import typing as ty
from jinja2 import Environment, PackageLoader, select_autoescape

from ankiwiktionary.wiktionary_parser import Word
from ankiwiktionary.reverso_parser import Synonym

env = Environment(
    loader=PackageLoader('ankiwiktionary', 'card_styles'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_card_from_word(word: Word):
    for meaning in word.meanings:
        if len(meaning.examples) > 3:
            meaning.examples = meaning.examples[:3]
    template = env.get_template('card_body_template.html')
    t = template.render(word=word)
    return t


def generate_synonyms_card(word: str, synonyms: ty.List[Synonym]):
    template = env.get_template('synonym_body_template.md')
    t = template.render(word=word, synonyms=synonyms)
    return t
