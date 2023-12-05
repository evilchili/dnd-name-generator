from language import defaults, types
from language.languages.elvish import Language
from language.languages.elvish.base import suffixes

PlaceName = types.NameGenerator(
    language=Language,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel,vowel|consonant,vowel|consonant"), 1.0),
        (types.Syllable(template="consonant,vowel|consonant,vowel|consonant"), 0.3),
    ),
    templates=types.NameSet(
        (types.NameTemplate("affix,name"), 1.0),
    ),
    affixes=types.WeightedSet(("el", 1.0)),
    adjectives=defaults.adjectives,
    suffixes=suffixes,
)


class ElvishNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            syllables=Language.syllables,
            templates=types.NameSet(
                (types.NameTemplate("name,affix,surname"), 1.0),
            ),
            affixes=types.equal_weights(["am", "an", "al", "um"], weight=1.0, blank=False),
            adjectives=defaults.adjectives,
            titles=defaults.titles,
            suffixes=suffixes,
        )
        self.language.minimum_grapheme_count = 2
        self.place_generator = PlaceName

    def get_surname(self) -> str:
        return self.place_generator.name()[0]["name"][0]


class NobleElvishNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            syllables=Language.syllables,
            templates=types.NameSet(
                (types.NameTemplate("name,name,affix,surname"), 1.0),
            ),
            affixes=types.equal_weights(["am", "an", "al", "um"], weight=1.0, blank=False),
            adjectives=defaults.adjectives,
            titles=defaults.titles,
        )
        self.language.minimum_grapheme_count = 2
        self.place_generator = PlaceName
        self.suffixes = types.equal_weights(
            [
                "ieth",
                "ies",
                "ier",
                "ien",
                "iath",
                "ias",
                "iar",
                "ian",
                "ioth",
                "ios",
                "ior",
                "ion",
            ],
            1.0,
            blank=False
        )

    def get_surname(self) -> str:
        return self.place_generator.name()[0]["name"][0] + self.suffixes.random()


Name = ElvishNameGenerator()
NobleName = NobleElvishNameGenerator()
