import logging
import os
import random
from enum import Enum
from types import ModuleType

import language

import typer
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer()

app_state = {}

default_language = os.environ.get("FANLANG_DEFAULT_LANGUAGE", "common")
language_pack, supported_languages = language.load_language_pack()

Supported = Enum("Supported", ((k, k) for k in supported_languages.keys()))


def print_sample(lang: str, module: ModuleType) -> None:
    summary = module.__doc__.replace("\n", "  \n")
    print(f"{summary}")
    print(f"  Text:        {module.Language.text(10)}")
    print(f"  Names:       {module.Name}")
    print(f"               {module.Name}")
    print(f"               {module.Name}")
    if module.NobleName != module.Name:
        print(f"  Noble Names: {module.NobleName}")
        print(f"               {module.NobleName}")
        print(f"               {module.NobleName}")
        print("")


@app.callback()
def main(
    language: Supported = typer.Option(
        default=default_language,
        help="The language to use."
    ),
):
    app_state["language"] = supported_languages[language.name]

    debug = os.getenv("FANLANG_DEBUG", None)
    logging.basicConfig(
        format="%(name)s %(message)s",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )
    logging.getLogger('markdown_it').setLevel(logging.ERROR)
    logging.debug(f"Loaded language pack {language_pack}.")
    logging.debug(f"Default language: {default_language}.")


@app.command()
def text(count: int = typer.Option(50, help="The number of words to generate.")):

    phrases = []
    phrase = []
    for word in app_state["language"].Language.word(count):
        phrase.append(str(word))
        if len(phrase) >= random.randint(1, 12):
            phrases.append(' '.join(phrase))
            phrase = []
    if phrase:
        phrases.append(' '.join(phrase))

    paragraph = phrases[0].capitalize()
    for phrase in phrases[1:]:
        if random.choice([0, 0, 1]):
            paragraph = paragraph + random.choice('?!.') + ' ' + phrase.capitalize()
        else:
            paragraph = paragraph + ', ' + phrase
    paragraph = paragraph + random.choice('?!.')

    console = Console(width=80)
    console.print(paragraph)


@app.command()
def names(
    count: int = typer.Option(50, help="The number of names to generate."),
    noble: bool = typer.Option(False, help="Generate noble names."),
):
    generator = app_state["language"].Name if not noble else app_state["language"].NobleName
    for name in generator.name(count):
        print(name["fullname"])


@app.command()
def list():
    console = Console(width=80)
    for lang, module in supported_languages.items():
        console.print(Markdown(module.__doc__))


if __name__ == "__main__":
    app()
