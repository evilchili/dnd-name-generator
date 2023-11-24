from language import types
from language.languages.lizardfolk import Language


class LizardfolkNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            templates=types.NameSet(
                (types.NameTemplate("surname,name,name"), 1.0),
            ),
        )

    def get_surname(self) -> str:
        return self.language.consonants.random().title()


Name = LizardfolkNameGenerator()
NobleName = Name
