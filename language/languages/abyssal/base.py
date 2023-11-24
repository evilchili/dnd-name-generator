from language import defaults, types

vowels = types.equal_weights(["a", "e", "i"], 1.0, blank=False)
consonants = types.equal_weights(["z", "sh", "s", "wh", ".."], 1.0, blank=False)

Language = types.Language(
    name="celstial",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=None,
    rules=[],
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel|consonant") * 10, 1.0),
        (types.Syllable(template="vowel|consonant") * 15, 1.0),
        (types.Syllable(template="vowel|consonant") * 20, 1.0),
    ),
)
