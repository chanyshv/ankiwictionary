from jinja2 import Environment, PackageLoader, select_autoescape

from ankiwiktionary.parser import Word

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
