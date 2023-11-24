import logging
import os
from enum import Enum
from types import ModuleType


import typer
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown

from language import supported_languages

app = typer.Typer()

app_state = {}

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
    language: Supported = typer.Option("common", help="The language to use."),
):
    app_state["language"] = supported_languages[language.name]

    debug = os.getenv("DEBUG", None)
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )


@app.command()
def words(count: int = typer.Option(50, help="The number of words to generate.")):
    print(" ".join(list(app_state["language"].Language.word(count))))


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
