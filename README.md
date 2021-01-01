CLI for generating Anki flashcards from wiktionary.org pages. **Works only with russian words**.

# ankiwiktionary

```
Usage: ankiwiktionary [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen-cards  Generate flashcards from passed WORDS
  search     Search for the passed WORDS in wiktionary
```

## Features

* Generating cloze cards
* Examples processing

## Usage

```commandline
➜  tmp ankiwiktionary gen-cards самоопределяться луддит дихотомия привинтивный дискурс конструктивный
Word "самоопределяться" processed successfully
Word "луддит" processed successfully
Word "дихотомия" processed successfully
[Error] Word "привинтивный" not found
Word "дискурс" processed successfully
Word "конструктивный" processed successfully
➜  tmp ankiwiktionary search привинтивный
Results for "привинтивный":
➜  tmp ankiwiktionary search люмпед
Results for "люмпед": люмпен, люмпен-пролетариат, люмпенизация, люмпен-пролетарий, люмпен-интеллигенция, люмпенский, люмпенизироваться, люмпенизировать, люмпенствовать, люмпен-интеллигент
```

## Important details

* Generated file should be imported to Anki using "Import File" button. Set "Fields separated by" to `~` and activate the "Allow HTML in fields" checkbox.