from language import types
from language.languages.gnomish import Language

Name = types.NameGenerator(
    language=Language,
    templates=types.NameSet(
        (types.NameTemplate("name,surname"), 1.0),
    ),
)
NobleName = Name
