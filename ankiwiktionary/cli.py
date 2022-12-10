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


@ankiwiktionary.command('synonyms', help='Search for synonyms of the passed words in Wiktionary')
@click.argument('words', nargs=-1)
@click.option('--result_dir', '-r', type=click.Path(writable=True), default='.',
              help='Path to the file to write the result to')
@click.pass_context
def gen_synonym_cards(ctx: click.Context, words: ty.Sequence[str], result_dir: str):
    term: Terminal = ctx.obj['terminal']
    for word in words:
        print(f'Processing word {Fore.MAGENTA + word + Style.RESET_ALL}')
        synonyms = ctx.obj['synonyms_client'].get_synonyms(word)
        if not synonyms:
            print("No synonyms found")
            continue
        for i, synonym in enumerate(synonyms):
            print(f'{i + 1}: {synonym}')
        while 1:
            print("Print numbers of synonyms to include in the card, separated by space")
            numbers = list(map(int, input().split()))
            if (not numbers) or (not all(0 < n <= len(synonyms) for n in numbers)):
                print("Invalid input")
                continue
            print("Picked words are:")
            for n in numbers:
                print(f'{n}: {synonyms[n - 1]}')
            if not click.confirm('Confirm?'):
                continue
            else:
                break
        other_synonyms = []
        if click.confirm("Add any other synonyms?"):
            other_synonyms = input().split()
        taken_synonyms = [synonyms[n - 1] for n in numbers]
        taken_synonyms.extend(other_synonyms)
        processed_words = []
        for synonym_ind, synonym in enumerate(taken_synonyms):
            parsed_syn = _process_wiktionary_word(synonym, ctx.obj['client'])
            if not parsed_syn:
                continue
            parsed_syn.word = parsed_syn.word.capitalize()

            # processing meanings and examples
            k = 0
            print(f"There are {len(parsed_syn.meanings)} meanings for this word")
            examples = []
            for i, meaning in enumerate(parsed_syn.meanings):
                print(f'{Fore.MAGENTA + str(i + 1) + Style.RESET_ALL}: {term.italic(meaning.definition)}')
                for _, ex in enumerate(meaning.examples):
                    print(f'\t{Fore.CYAN + str(k + 1) + Style.RESET_ALL}: {ex}')
                    examples.append(ex)
                    k += 1
            example = None
            while 1:
                print("Which should be included in the card? (0 to provide your own, -1 to skip)")
                n = int(input())
                if n == -1:
                    break
                if n == 0:
                    example = input()
                    break
                if not 0 < n <= len(examples):
                    print("Invalid input")
                    continue
                example = examples[n - 1]
                break
            if example is None:
                continue

            # processing cloze
            print("Which words should be clozed?")
            print(_sentence_to_replaced(example, parsed_syn.word))
            words = example.split()
            clozed_words_indexes = list(map(int, input().split()))
            clozed_words = [words[i - 1].strip(".,?!") for i in clozed_words_indexes]
            for ww in clozed_words:
                example = example.replace(ww, f'{{{synonym_ind + 1}|{ww}}}')
            processed_words.append(Synonym(parsed_syn.word, example))
        word = word.capitalize()
        card = generate_synonyms_card(word, processed_words)
        with open(Path(result_dir) / f'{word}.md', 'w') as f:
            f.write(card)


def _sentence_to_replaced(sentence: str, word: str):
    w_l = len(word)
    spl = sentence.split()
    r = []
    for i, s in enumerate(spl):
        if 0.7 <= w_l / len(s) <= 1.5:
            r.append(f'{i + 1}: {Fore.MAGENTA + s + Style.RESET_ALL}')
        else:
            r.append(f'{s}')
    return ' '.join(r)


def main():
    ankiwiktionary(obj={})
