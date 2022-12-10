TARGET DECK: Слова
START
Cloze
# {{ word }}
{% for synonym in synonyms %}{{ loop.index }}. {{ '{' }}{{ loop.index }}|{{ synonym.word }}}
    {{synonym.example}}
{% endfor %}
END
#synonim
