from language import defaults, types
from language.languages.dwarvish import Language


class DwarvishNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                # (types.NameTemplate("adjective,name,nickname,surname"), 1.0),
                (types.NameTemplate("adjective,name,surname"), 1.0),
            ),
            affixes=None,
            adjectives=defaults.adjectives,
            titles=defaults.titles,
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(["son", "sson", "zhon", "dottir", "dothir", "dottyr"], 1.0)

    def get_surname(self) -> str:
        return super().get_surname() + self.suffixes.random()


Name = DwarvishNameGenerator()
NobleName = Name
