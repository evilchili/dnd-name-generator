from language import defaults, types

from .rules import rules

vowels = defaults.vowels + types.equal_weights(["ä", "ö", "ü", "äu"], 0.5, blank=False)
prefixes = defaults.vowels + types.equal_weights(["c", "g", "l", "m", "n", "r", "s", "t", "v", "z"], 1.0, blank=False)
suffixes = types.equal_weights(["a", "e", "i", "t", "s", "m", "n", "l", "r", "d", "a", "th"], 1.0, blank=False)

Language = types.Language(
    name="undercommon",
    vowels=vowels,
    consonants=defaults.consonants,
    prefixes=prefixes,
    suffixes=suffixes,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel,consonant,vowel") * 2, 0.15),
        (types.Syllable(template="consonant|vowel,consonant,vowel,consonant,vowel"), 1.0),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
