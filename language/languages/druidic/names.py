from language import types
from language.languages.druidic import Language

Name = types.NameGenerator(
    language=Language,
    templates=types.NameSet(
        (types.NameTemplate("name"), 1.0),
    ),
)


class DruidicNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("name"), 1.0),
            ),
        )
        self.language.minimum_grapheme_count = 2


class NobleDruidicNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("name"), 1.0),
            ),
        )
        self.language.minimum_grapheme_count = 2
        self.suffixes = types.equal_weights(["as", "es", "is", "os", "us"], 1.0, blank=False)

    def get_name(self) -> str:
        return super().get_name() + self.suffixes.random()


Name = DruidicNameGenerator()
NobleName = NobleDruidicNameGenerator()
