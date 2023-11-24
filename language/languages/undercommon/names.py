import random

from language import defaults, types
from language.languages.undercommon import Language

PlaceName = types.NameGenerator(
    language=Language,
    syllables=Language.syllables,
    templates=types.NameSet(
        (types.NameTemplate("affix,name"), 1.0),
    ),
    affixes=types.WeightedSet(("el", 1.0)),
    adjectives=defaults.adjectives,
    suffixes=Language.suffixes,
)


class DrowName(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            syllables=Language.syllables,
            templates=types.NameSet(
                (types.NameTemplate("name,surname"), 1.0),
            ),
        )
        self.language.minimum_grapheme_count = 2
        self.place_generator = PlaceName
        self.affixes = types.equal_weights(["am", "an", "al", "um"], weight=1.0, blank=False)

    def get_surname(self) -> str:
        name = self.place_generator.name()[0]["name"][0]
        return (self.affixes.random() + name + random.choice(["th", "s", "r", "n"])).title()


Name = DrowName()
NobleName = Name
