import logging
import os
import textwrap
from enum import Enum
from types import ModuleType

import language

import typer
from rich.logging import RichHandler
from rich.console import Console

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

    paragraph = app_state["language"].Language.text(count)

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
def list(names: bool = typer.Option(False, help="Display sample names.")):
    for lang, module in supported_languages.items():
        if names:
            text = str(module.Name)
        else:
            text = textwrap.shorten(module.Language.text(count=20), width=70, placeholder='')
        print(f"{lang.title():15s}: {text}")


if __name__ == "__main__":
    app()
