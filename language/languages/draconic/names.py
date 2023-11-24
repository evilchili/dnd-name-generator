from language import defaults, types
from language.languages.draconic import Language

# dragon_titles = types.equal_weights([
# ], 1.0)


class DraconicNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("name"), 1.0),
                (types.NameTemplate("adjective,name"), 1.0),
            ),
            adjectives=defaults.adjectives,
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(["us", "ius", "eus", "a", "an", "is"], 1.0, blank=False)

    def get_name(self) -> str:
        return super().get_name() + self.suffixes.random()


class NobleDraconicNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("surname,the,title"), 1.0),
            ),
            # titles=dragon_titles,
            syllables=types.SyllableSet(
                (types.Syllable(template="consonant|vowel") * 2, 1.0),
            ),
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(
            [
                "thus",
                "thux",
                "thas",
                "thax",
                "this",
                "thix",
                "thes",
                "thex",
                "xus",
                "xux",
                "xas",
                "xax",
                "xis",
                "xix",
                "xes",
                "xex",
                "ssus",
                "ssux",
                "ssas",
                "ssax",
                "ssis",
                "ssix",
                "sses",
                "ssex",
                "zus",
                "zux",
                "zas",
                "zax",
                "zis",
                "zix",
                "zes",
                "zex",
            ],
            1.0,
            blank=False,
        )

    def get_title(self) -> str:
        p = ""
        while not p:
            p = defaults.personality.random()
        return p

    def get_surname(self) -> str:
        return super().get_name().replace("'", "").title() + self.suffixes.random()


Name = DraconicNameGenerator()
NobleName = NobleDraconicNameGenerator()
