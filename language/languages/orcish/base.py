from language import defaults, types

from .rules import rules

consonants = types.WeightedSet(
    ("b", 1.0),
    ("c", 1.0),
    ("d", 1.0),
    ("f", 0.5),
    ("h", 1.0),
    ("k", 1.0),
    ("m", 0.3),
    ("n", 0.3),
    ("p", 1.0),
    ("r", 0.2),
    ("s", 0.1),
    ("t", 1.0),
    ("z", 1.0),
    ("ch", 1.0),
    ("sh", 0.7),
    ("br", 1.0),
)

Language = types.Language(
    name="orcish",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=None,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant,vowel") * 2, 1.0),
        (types.Syllable(template="consonant,vowel,consonant,vowel,consonant"), 0.5),
    ),
    rules=rules,
    minimum_grapheme_count=1,
)
