from language import types

from .rules import rules

vowels = types.WeightedSet(
    ("a", 1.0),
    ("e", 1.0),
    ("i", 0.3),
    ("o", 0.8),
    ("u", 0.7),
    ("y", 0.3),
    ("j", 0.05),
    ("î", 0.3),
    ("ê", 1.0),
    ("â", 1.0),
    ("û", 1.0),
)
consonants = types.WeightedSet(
    ("b", 0.3),
    ("c", 0.5),
    ("d", 1.0),
    ("f", 0.5),
    ("k", 1.0),
    ("l", 0.3),
    ("m", 0.3),
    ("n", 0.3),
    ("p", 1.0),
    ("s", 1.0),
    ("t", 1.0),
    ("v", 0.5),
    ("w", 0.5),
    ("y", 0.3),
    ("ph", 1.0),
    ("th", 1.0),
    ("ch", 1.0),
    ("kh", 1.0),
    ("zh", 1.0),
    ("sh", 1.0),
)

Language = types.Language(
    name="dwarvish",
    vowels=vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=None,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant,vowel|consonant") * 1, 1.0),
        (types.Syllable(template="consonant,vowel|consonant") * 2, 0.5),
        (types.Syllable(template="consonant,vowel|consonant") * 3, 0.2),
    ),
    rules=rules,
    minimum_grapheme_count=1,
)
