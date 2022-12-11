TARGET DECK: Слова
START
Cloze
# {{ word }}
{% for synonym in synonyms %}{{ loop.index }}. {{ '{' }}{{ loop.index }}|{{ synonym.word.capitalize() }}}
    _{{synonym.example}}_
{% endfor %}
END
#synonim
