from language import types
from language.languages.celestial import Language

Name = types.NameGenerator(
    language=Language,
    templates=types.NameSet(
        (types.NameTemplate("name"), 1.0),
    ),
)

NobleName = Name
