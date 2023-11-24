from language import types

scents = types.equal_weights(
    [
        "honey",
        "caramel",
        "maple syrup",
        "molasses",
        "dark chocolate",
        "chocolate",
        "almond",
        "hazelnut",
        "peanut",
        "clove",
        "cinnamon",
        "nutmeg",
        "anise",
        "malt",
        "grain",
        "roast",
        "smoke",
        "ash",
        "acrid",
        "rubber",
        "skunk",
        "petroleum",
        "medicine",
        "salt",
        "bitter",
        "phrenolic",
        "meat",
        "broth",
        "animal",
        "musty",
        "earth",
        "mould",
        "damp",
        "wood",
        "paper",
        "cardboard",
        "stale",
        "herb",
        "hay",
        "grass",
        "peapod",
        "whisky",
        "wine",
        "malic",
        "citric",
        "isovaleric",
        "butyric",
        "acetic",
        "lime",
        "lemon",
        "orange",
        "grapefruit",
        "pear",
        "peach",
        "apple",
        "grape",
        "pineapple",
        "pomegranate",
        "cherry",
        "coconut",
        "prune",
        "raisin",
        "strawberry",
        "blueberry",
        "raspberry",
        "blackberry",
        "jasmine",
        "rose",
        "camomile",
        "tobacco",
    ],
    1.0,
    blank=False,
)

family = types.equal_weights(
    [
        "sweet",
        "floral",
        "fruity",
        "sour",
        "fermented",
        "green",
        "vegetal",
        "old",
        "roasted",
        "spiced",
        "nutty",
        "cocoa",
        "pepper",
        "pungent",
        "burnt",
        "carmelized",
        "raw",
        "rotting",
        "dead",
        "young",
    ],
    1.0,
    blank=False,
)

Language = types.Language(
    name="lizardfolk",
    vowels=scents,
    consonants=family,
    prefixes=None,
    suffixes=None,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel"), 1.0),
    ),
    rules=(),
    minimum_grapheme_count=1,
)
