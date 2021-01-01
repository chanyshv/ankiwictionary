import csv
import typing as ty

import click
import colorama
import requests as rq

from .main import generate_card_from_word
from .parser import Wictionary, NotFoundError


def _generate_error_message(error_text: str) -> str:
    return f'[{colorama.Fore.RED + "Error" + colorama.Style.RESET_ALL}] {error_text}'


@click.group()
@click.pass_context
def ankiwictionary(ctx: click.Context):
    colorama.init()
    client = Wictionary()
    ctx.obj['client'] = client


@ankiwictionary.command('gen-cards')
@click.argument('words', nargs=-1)
@click.option('--result_path', '-r', type=click.Path(writable=True))
@click.pass_context
def gen_cards(ctx: click.Context, words: ty.Sequence[str], result_path):
    with open(result_path or './wictionary-result.csv', 'w', newline='') as fp:
        writer = csv.writer(fp, delimiter='~', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for word_str in words:
            try:
                w = ctx.obj['client'].get_word(word_str)
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
            writer.writerow((generate_card_from_word(w),))
            print(f'Word "{word_str}" processed {colorama.Fore.GREEN + "successfully" + colorama.Style.RESET_ALL}')


@ankiwictionary.command('search')
@click.argument('words', nargs=-1)
@click.pass_context
def search(ctx: click.Context, words: ty.Sequence[str]):
    client: Wictionary = ctx.obj['client']
    for word in words:
        results = client.search(word)
        print(f'Results for "{word}": {", ".join(results)}')
