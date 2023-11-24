from language import types

from .rules import rules

vowels = types.equal_weights(["a'", "e'", "i'", "o'"], 1.0, blank=False) + types.equal_weights(
    ["a", "e", "i", "o", "y"], 0.5, blank=False
)

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
    name="halfling",
    vowels=vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=suffixes,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant,vowel") * 2, 0.5),
        (types.Syllable(template="consonant,vowel") * 3, 0.75),
        (types.Syllable(template="consonant,vowel") * 4, 1.0),
        (types.Syllable(template="consonant,vowel") * 5, 1.0),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
