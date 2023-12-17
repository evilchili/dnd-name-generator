from language import types

from .rules import rules

# surexit tutbulc filius liuit hagener tutri dierchi tir telih haioid ilau elcu
# filius gelhig haluidt iuguret amgucant pel amtanndi ho diued diprotant gener
# tutri o guir imguodant ir degion guragon tagc rodesit elcu guetig equs tres
# uache, tres uache nouidligi namin ir ni be cas igridu dimedichat guetig hit
# did braut grefiat guetig nis minn tutbulc hai cenetl in ois oisau

consonants = types.WeightedSet(
    ("b", 0.2),
    ("c", 0.8),
    ("d", 0.5),
    ("f", 0.2),
    ("g", 1.0),
    ("h", 0.5),
    ("l", 1.0),
    ("m", 0.5),
    ("n", 1.0),
    ("p", 0.5),
    ("r", 1.0),
    ("s", 0.8),
    ("t", 1.0),
    ("ll", 0.5),
    ("dd", 0.5),
)

vowels = types.WeightedSet(
    ("a", 0.8),
    ("e", 0.5),
    ("i", 1.0),
    ("o", 0.5),
    ("u", 1.0)
)

suffixes = types.equal_weights(
    [
        "t",
        "lc",
        "r",
        "h",
        "g",
        "i",
        "s",

    ],
    0.5,
    blank=True,
)

Language = types.Language(
    name="druidic",
    vowels=vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=suffixes,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel"), 0.3),
        (types.Syllable(template="consonant,vowel"), 0.33),
        (types.Syllable(template="consonant|vowel,vowel"), 0.33),
        (types.Syllable(template="consonant|vowel,vowel,consonant|vowel"), 1.0),
        (types.Syllable(template="consonant,vowel,vowel,consonant,vowel"), 1.0),
    ),
    rules=rules,
    minimum_grapheme_count=1,
)
