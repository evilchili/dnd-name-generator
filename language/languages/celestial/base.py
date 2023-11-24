from language import defaults, types

vowels = types.equal_weights(["a", "e", "i", "o", "u"], 1.0, blank=False)
consonants = types.equal_weights(
    ["î", "ê", "â", "û", "ô", "ä", "ö", "ü", "äu", "ȧ", "ė", "ị", "ȯ", "u̇"], 1.0, blank=False
)

Language = types.Language(
    name="celstial",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=None,
    rules=[],
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel|consonant") * 20, 1.0),
        (types.Syllable(template="vowel|consonant") * 25, 1.0),
        (types.Syllable(template="vowel|consonant") * 30, 1.0),
        (types.Syllable(template="vowel|consonant") * 35, 1.0),
    ),
)
