import csv
import typing as ty
from pathlib import Path

import click
import colorama
import requests as rq
from colorama import Fore, Style
from blessings import Terminal

from .main import (
    generate_card_from_word,
    generate_synonyms_card,
)
from .wiktionary_parser import (
    Wiktionary,
    NotFoundError,
    Word,
)
from .reverso_parser import (
    ReversoSynonyms,
    Synonym,
)


def _generate_error_message(error_text: str) -> str:
    return f'[{colorama.Fore.RED + "Error" + colorama.Style.RESET_ALL}] {error_text}'


@click.group()
@click.pass_context
def ankiwiktionary(ctx: click.Context):
    colorama.init()
    client = Wiktionary()
    ctx.obj['client'] = client
    ctx.obj['synonyms_client'] = ReversoSynonyms()
    ctx.obj['terminal'] = Terminal()


@ankiwiktionary.command('gen-cards', help='Generate flashcards from passed WORDS')
@click.argument('words', nargs=-1)
@click.option('--result_path', '-r', type=click.Path(writable=True), default='./wiktionary-result.csv',
              help='Path to the file to write the result to')
@click.pass_context
def gen_cards(ctx: click.Context, words: ty.Sequence[str], result_path):
    with open(result_path, 'w', newline='') as fp:
        writer = csv.writer(fp, delimiter='~', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for word_str in words:
            try:
                w: Word = ctx.obj['client'].get_word(word_str.lower())
            except NotFoundError:
                print(_generate_error_message(f'Word "{word_str}" not found'))
                continue
            except rq.RequestException:
                print(_generate_error_message(
                    f'Word "{word_str}" was not processed. Network issues - server is not reachable'))
                continue
            except Exception:
                print(_generate_error_message(f'Word "{word_str}" was not processed. Unknown error'))
                continue
            w.word = w.word.capitalize()
            writer.writerow((generate_card_from_word(w),))
            print(f'Word "{word_str}" processed {colorama.Fore.GREEN + "successfully" + colorama.Style.RESET_ALL}')


@ankiwiktionary.command('search', help='Search for the passed WORDS in wiktionary')
@click.argument('words', nargs=-1)
@click.pass_context
def search(ctx: click.Context, words: ty.Sequence[str]):
    client: Wiktionary = ctx.obj['client']
    for word in words:
        results = client.search(word)
        print(f'Results for "{word}": {", ".join(results)}')


def _process_wiktionary_word(word, client: Wiktionary):
    print(f'Processing word: "{Fore.MAGENTA + word + Style.RESET_ALL}"')
    w = None
    try:
        w: Word = client.get_word(word.lower())
    except NotFoundError:
        print(_generate_error_message(f'Word "{word}" not found'))
    except rq.RequestException:
        print(_generate_error_message(
            f'Word "{word}" was not processed. Network issues - server is not reachable'))
    except Exception:
        print(_generate_error_message(f'Word "{word}" was not processed. Unknown error'))
    return w


def _input_synonyms(word, synonyms: ty.Sequence[str]):
    print(f'Processing word {Fore.MAGENTA + word + Style.RESET_ALL}')
    if not synonyms:
        print("No synonyms found")
        return []
    for i, synonym in enumerate(synonyms):
        print(f'{i + 1}: {synonym}')
    while 1:
        print("Print numbers of synonyms to include in the card, separated by space (0 to skip)")
        numbers = list(map(int, input().split()))
        if (not numbers) or (not all(0 < n <= len(synonyms) for n in numbers)):
            if numbers and numbers[0] == 0:
                return []
            print("Invalid input")
            continue
        return [synonyms[n - 1] for n in numbers]


def _provide_own_example(skip=False):
    print("Print your own example" + " (0 to skip)" if skip else "")
    inp = input()
    if skip and inp == '0':
        return None
    return inp


def _print_meanings(parsed_syn: Word, term: Terminal):
    k = 0
    print(f"There are {len(parsed_syn.meanings)} meanings for this word")
    for i, meaning in enumerate(parsed_syn.meanings):
        print(f'{Fore.MAGENTA + str(i + 1) + Style.RESET_ALL}: {term.italic(meaning.definition)}')
        for _, ex in enumerate(meaning.examples):
            print(f'\t{Fore.CYAN + str(k + 1) + Style.RESET_ALL}: {ex}')
            k += 1


def _input_for_example(examples: ty.Sequence[str]):
    while 1:
        print("Which should be included in the card? (0 to provide your own, -1 to skip)")
        inp = input()
        if not inp.isdigit():
            print("Invalid input")
            continue
        n = int(inp)
        if n == -1:
            break
        if n == 0:
            return _provide_own_example()
        if not 0 < n <= len(examples):
            print("Invalid input")
            continue
        return examples[n - 1]


def _cloze_example(example, synonym, synonym_ind):
    print("Which words should be clozed?")
    print(_sentence_to_replaced(example, synonym))
    words = example.split()
    clozed_words_indexes = list(map(int, input().split()))
    clozed_words = [words[i - 1].strip(".,?!") for i in clozed_words_indexes]
    for ww in clozed_words:
        example = example.replace(ww, f'{{{synonym_ind + 1}|{ww}}}')
    example = example.replace(f'}} {{{synonym_ind + 1}|', ' ')
    return example


@ankiwiktionary.command('synonyms', help='Search for synonyms of the passed words in Wiktionary')
@click.argument('words', nargs=-1)
@click.option('--result_dir', '-r', type=click.Path(writable=True), default='.',
              help='Path to the file to write the result to')
@click.pass_context
def gen_synonym_cards(ctx: click.Context, words: ty.Sequence[str], result_dir: str):
    term: Terminal = ctx.obj['terminal']
    for word in words:
        taken_synonyms = _input_synonyms(word, ctx.obj['synonyms_client'].get_synonyms(word))
        other_synonyms = []
        if click.confirm("Add any other synonyms?"):
            other_synonyms = input().split()
        taken_synonyms.extend(other_synonyms)
        processed_words = []
        for synonym_ind, synonym in enumerate(taken_synonyms):
            parsed_syn = _process_wiktionary_word(synonym, ctx.obj['client'])
            examples = []
            if parsed_syn:
                _print_meanings(parsed_syn, term)
                examples = [ex for meaning in parsed_syn.meanings for ex in meaning.examples]
                if examples:
                    example = _input_for_example(examples)
            if not examples or not parsed_syn:
                example = _provide_own_example(skip=True)
            processed_words.append(Synonym(synonym, _cloze_example(example.strip(), synonym, synonym_ind)))
        word = word.capitalize()
        card = generate_synonyms_card(word, processed_words)
        with open(Path(result_dir) / f'{word}.md', 'w') as f:
            f.write(card)


def _sentence_to_replaced(sentence: str, word: str):
    spl = sentence.split()
    r = []
    mnw = (min(len(w) for w in word.split()))
    mxw = (max(len(w) for w in word.split()))
    for i, s in enumerate(spl):
        if 0.7 <= len(s) / mnw and len(s) / mxw <= 1.5:
            r.append(f'{i + 1}: {Fore.MAGENTA + s + Style.RESET_ALL}')
        else:
            r.append(f'{s}')
    return ' '.join(r)


def main():
    ankiwiktionary(obj={})
