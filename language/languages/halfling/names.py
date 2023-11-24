from language import defaults, types
from language.languages.halfling import Language


class HalflingNameGenerator(types.NameGenerator):
    def get_name(self) -> str:
        return super().get_name().lower().capitalize()


Name = HalflingNameGenerator(
    language=Language,
    nicknames=defaults.positive_adjectives,
    templates=types.NameSet(
        (types.NameTemplate("name,name,name,nickname"), 1.0),
    ),
)
NobleName = Name
