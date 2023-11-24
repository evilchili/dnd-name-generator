from language import defaults, types

from .rules import rules

consonants = types.WeightedSet(
    ("b", 1.0),
    ("c", 1.0),
    ("d", 1.0),
    ("f", 0.5),
    ("g", 0.5),
    ("j", 1.0),
    ("k", 1.0),
    ("l", 0.3),
    ("m", 0.3),
    ("n", 0.3),
    ("p", 1.0),
    ("r", 0.2),
    ("s", 0.1),
    ("t", 1.0),
    ("v", 1.0),
    ("x", 1.0),
    ("y", 1.0),
    ("z", 1.0),
)

prefixes = types.equal_weights(
    [
        "t'",
        "x'",
        "k'",
        "p'",
        "z'",
    ],
    0.5,
)

Language = types.Language(
    name="infernal",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=prefixes,
    suffixes=None,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant|vowel") * 2, 0.05),
        (types.Syllable(template="consonant|vowel") * 3, 1.0),
        (types.Syllable(template="consonant|vowel") * 4, 0.75),
        (types.Syllable(template="consonant|vowel") * 5, 0.5),
        (types.Syllable(template="consonant|vowel") * 6, 0.25),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
