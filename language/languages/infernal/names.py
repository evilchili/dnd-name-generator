from language import types
from language.languages.infernal import Language

adjectives = types.equal_weights(
    [
        "eternal",
        "wondrous",
        "luminous",
        "perfect",
        "essential",
        "golden",
        "unfailing",
        "perpetual",
        "infinite",
        "exquisite",
        "sinless",
        "ultimate",
        "flawless",
        "timeless",
        "glorious",
        "absolute",
        "boundless",
        "true",
        "incredible",
        "virtuous",
        "supreme",
        "enchanted",
        "magnificent",
        "superior",
        "spectacular",
        "divine",
    ],
    0.25,
)

bloodlines = types.equal_weights(
    [
        "Asmodeus",
        "Baalzebul",
        "Rimmon",
        "Dispater",
        "Fierna",
        "Glasya",
        "Levistus",
        "Mammon",
        "Mephistopheles",
        "Zariel",
    ]
)


class InfernalNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                # (types.NameTemplate("adjective,name,nickname,surname"), 1.0),
                (types.NameTemplate("name"), 0.25),
                (types.NameTemplate("adjective,name"), 0.25),
            ),
            adjectives=adjectives,
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(["us", "ius", "eus", "a", "an", "is"], 1.0, blank=False)

    def get_name(self) -> str:
        return super().get_name() + self.suffixes.random()


class NobleInfernalNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("adjective,name"), 1.0),
            ),
            adjectives=bloodlines,
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(["us", "ius", "to", "tro", "eus", "a", "an", "is"], 1.0, blank=False)

    def get_name(self) -> str:
        return super().get_name() + self.suffixes.random()


Name = InfernalNameGenerator()
NobleName = NobleInfernalNameGenerator()
