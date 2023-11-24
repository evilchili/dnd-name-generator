from language import defaults, types

from .rules import rules

consonants = types.WeightedSet(
    ("b", 0.5),
    ("d", 0.5),
    ("f", 0.3),
    ("g", 0.3),
    ("h", 0.5),
    ("j", 0.2),
    ("l", 1.0),
    ("m", 0.5),
    ("n", 1.0),
    ("p", 0.5),
    ("r", 1.0),
    ("s", 1.0),
    ("t", 1.0),
    ("v", 0.3),
    ("w", 0.2),
    ("z", 0.1),
)

suffixes = types.equal_weights(
    [
        "a",
        "e",
        "i",
        "o",
        "y",
    ],
    1.0,
    blank=False,
)

Language = types.Language(
    name="gnomish",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=suffixes,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant,vowel,vowel"), 1.0),
        (types.Syllable(template="consonant,vowel"), 0.33),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
