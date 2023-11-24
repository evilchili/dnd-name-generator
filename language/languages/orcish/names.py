from language import defaults, types
from language.languages.orcish import Language


class OrcishNameGenerator(types.NameGenerator):
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
        self.suffixes = types.equal_weights(
            [
                "acht",
                "echt",
                "icht",
                "ocht",
                "ucht",
                "ak",
                "ek",
                "ik",
                "ok",
                "uk",
                "ach",
                "ech",
                "ich",
                "och",
                "uch",
                "atch",
                "etch",
                "itch",
                "otch",
                "utch",
                "azk",
                "ezk",
                "izk",
                "ozk",
                "uzk",
                "azh",
                "ezh",
                "izh",
                "ozh",
                "uzh",
            ],
            1.0,
            blank=False,
        )

    def get_surname(self) -> str:
        return self.language.add_grapheme(word="", template="consonant").strip().title() + self.suffixes.random()


Name = OrcishNameGenerator()
NobleName = Name
