CLI for generating Anki flashcards from wictionary.org pages. **Works only with russian words**.

# ankiwictionary

```
Usage: ankiwictionary [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen-cards  Generate flashcards from passed WORDS
  search     Search for the passed WORDS in wictionary
```

## Features

* Generating cloze cards
* Examples processing

## Usage

```commandline
➜  tmp ankiwictionary gen-cards самоопределяться луддит дихотомия привинтивный дискурс конструктивный
Word "самоопределяться" processed successfully
Word "луддит" processed successfully
Word "дихотомия" processed successfully
[Error] Word "привинтивный" not found
Word "дискурс" processed successfully
Word "конструктивный" processed successfully
➜  tmp ankiwictionary search привинтивный
Results for "привинтивный":
➜  tmp ankiwictionary search люмпед
Results for "люмпед": люмпен, люмпен-пролетариат, люмпенизация, люмпен-пролетарий, люмпен-интеллигенция, люмпенский, люмпенизироваться, люмпенизировать, люмпенствовать, люмпен-интеллигент
```

## Important details

* Generated file should be imported to Anki using "Import File" button. Set "Fields separated by" to `~` and activate the "Allow HTML in fields" checkbox.