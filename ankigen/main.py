from jinja2 import Environment, PackageLoader, select_autoescape

from ankigen.parser import Wictionary

env = Environment(
    loader=PackageLoader('ankigen', 'card_styles'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_card_from_word(word: str):
    client = Wictionary()
    w = client.get_word(word)
    template = env.get_template('card_body_template.html')
    t = template.render(word=w)
    open('res.html', 'w').write(t)
    return t
