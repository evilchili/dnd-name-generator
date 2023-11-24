from language import types

from .rules import rules

vowels = types.equal_weights(
    ["sa", "saa", "sah", "se", "see", "sei", "sey", "si", "sii", "sir", "so", "su", "suu"], 1.0, blank=False
)

consonants = types.WeightedSet(
    ("d", 1.0),
    ("f", 0.5),
    ("g", 0.5),
    ("h", 1.0),
    ("j", 1.0),
    ("k", 1.0),
    ("l", 0.3),
    ("n", 0.3),
    ("r", 0.2),
    ("t", 1.0),
    ("v", 1.0),
    ("x", 1.0),
    ("y", 1.0),
    ("z", 1.0),
)


class DraconicLanguage(types.Language):
    stops = types.equal_weights(["'"], 1.0)

    def get_grapheme_vowel(self) -> str:
        return self.stops.random() + self.vowels.random() + self.stops.random()


Language = DraconicLanguage(
    name="draconic",
    vowels=vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=None,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant|vowel") * 2, 0.2),
        (types.Syllable(template="consonant|vowel") * 3, 1.0),
        (types.Syllable(template="consonant|vowel") * 4, 1.0),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
