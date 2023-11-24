from language import defaults, types
from language.languages.common import Language

suffixes = types.equal_weights(
    [
        "berg",
        "borg",
        "borough",
        "bury",
        "berry",
        "by",
        "ford",
        "gard",
        "grave",
        "grove",
        "gren",
        "hardt",
        "hart",
        "heim",
        "holm",
        "land",
        "leigh",
        "ley",
        "ly",
        "lof",
        "love",
        "lund",
        "man",
        "mark",
        "ness",
        "olf",
        "olph",
        "quist",
        "rop",
        "rup",
        "stad",
        "stead",
        "stein",
        "strom",
        "thal",
        "thorpe",
        "ton",
        "vall",
        "wich",
        "win",
        "some",
        "smith",
        "bridge",
        "cope",
        "town",
        "er",
        "don",
        "den",
        "dell",
        "son",
    ]
)

Name = types.NameGenerator(
    language=Language,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel|consonant"), 0.01),
        (types.Syllable(template="consonant,vowel"), 0.2),
        (types.Syllable(template="consonant,vowel") * 2, 1.0),
    ),
    templates=types.NameSet(
        (types.NameTemplate("adjective,title,name,surname,count"), 1.0),
        (types.NameTemplate("title,name,name,surname,count"), 1.0),
        (types.NameTemplate("title,name,name,surname,surname,count"), 1.0),
    ),
    names=None,
    surnames=None,
    nicknames=None,
    adjectives=defaults.adjectives,
    titles=defaults.titles,
    counts=defaults.counts,
    suffixes=suffixes,
)
Name.language.prefixes = None
Name.language.suffixes = None

NobleName = Name
