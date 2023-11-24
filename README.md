# D&D Language Generator

This package is a fantasy language generator. By defining a number of characteristics about your imagined language -- the graphemes, their relative frequency distributions, the construction of syllables, and so on -- you can generate random but internally consistent gibberish that feels distinct, evocative, and appropriate to your setting.

## Quick Start

```
>>> from language imported supported_languages
>>> common = supported_languages['common']
>>> common.word(2)
['apsoo', 'nirtoet']
>>> common.text()
Proitsiiiy be itkif eesof detytaen. Ojaot tyskuaz apsoo nirtoet prenao.
>>> commoner = f"{common.Name}"
"Quiet" Gushi Murk Lirpusome
>>> common.Name.name()
{
    name: ['Gushi', 'Murk'],
    surname: ['Lirpusome'],
    adjective: ["Quiet"],
}
```

## Supported Languages

A number of D&D languages are defined, with rules built according to the
conventions established by my D&D group over several years of play in our
homebrew setting. You can find all supported languages [in the languages
submodule](language/languages/); each submodule contains a README that
describes the basic characteristics of the language, along with examples.

## Defining a Language

### Layout

A language consists of several submodules:

* `base.py`, which contains grapheme definitions and the `Language` subclasses;
* `names.py`, which defines the `NameGenerator` subclasses; and
* `rules.py`, which is optional but defines the rules all words in the language must follow.


### Language Construction

Let's look at a simple example, the Gnomish language. Here's the `Language`
subclass that would be defined in `base.py`:

```
from language import defaults, types
from .rules import rules

consonants = types.WeightedSet(
    ("b", 0.5), ("d", 0.5), ("f", 0.3), ("g", 0.3),
    ("h", 0.5), ("j", 0.2), ("l", 1.0), ("m", 0.5),
    ("n", 1.0), ("p", 0.5), ("r", 1.0), ("s", 1.0),
    ("t", 1.0), ("v", 0.3), ("w", 0.2), ("z", 0.1),
)

suffixes = types.equal_weights(["a", "e", "i", "o", "y"], 1.0, blank=False)


Language = types.Language(
    name="gnomish",
    vowels=defaults.vowels,
    consonants=consonants,
    prefixes=None,
    suffixes=suffixes,
    syllables=types.SyllableSet(
        (types.Syllable(template="consonant,vowel,vowel"), 1.0),
        (types.Syllable(template="consonant,vowel"), 0.33),
    ),
    rules=rules,
    minimum_grapheme_count=2,
)
```

#### Defining Graphemes

A Language definition includes *graphemes*, the basic building blocks of any
language. We start with **vowels**, **consonants**, which are required in every
language; Gnomish also includes **suffixes**, but no **prefixes**. Each
grapheme is a `WeightedSet`, which is like a regular set except its members
consist of a tuple of a string and a relative weight from 0.0 to 1.0. These
weights will be used when selecting a random grapheme.

Gnomish uses the default vowels, defined in [the
language.defaults](language/defaults.py) submodule, but define our consonants
with a subset of English consonants. By experimenting with different sets and
different weights, you can generate radically different feeling text output!

Gnomish also uses suffixes, which are graphemes added to the ends of words.
Here we use the helper function `types.equal_weights()`, which returns
a `WeightedSet` where each member is given the same weight. Normally this
function also inserts the grapheme `("", 1.0)` into the set, but we disable
this behaviour by specifying `blank=False`.

#### Defining Syllables

A syllable is a collection of graphemes, including at least one vowel. When we
create words, we select a random syllable template from a `SyllableSet`, which
is just a `WeightedSet` whose members are `Syllable` instances. Each `Syllable`
declares a `template`, and like graphemes, has a weight associated with it that
will make it more or less likely to be chosen for a word.

A syllable's template consists of a comma-separated string of grapheme names.
In Gnomish, we have two possible syllable templates, `consonant,vowel,vowel`
and the shorter `consonant,vowel`, which will be selected one third as often.

Templates can also support randomly-selected graphemes by joining two or more
grapheme types with a vertical bar, for example `vowel|consonant` would choose
one or the other; `vowel|consonant,vowel` would result in a vowel or
a consonant followed by a vowel.

### How Words Are Constructed:

The main interface for callers is word(), which returns a randomly-generated
word in the language according to the following algorithm:

1. Choose a random syllable from the syllable set
2. For each grapheme in the syllable
    3. Choose a random grapheme template
    4. Choose a random sequence from the language for that grapheme
    5. Validate the word against the language rules
6. Repeat 1-5 until a valid word is generated
7. Add a prefix and suffix, if they are defined

When graphemes are chosen, the following rules are applied:
* Every syllable must have at least one vowel; and
* A syllable may never have three consecutive consonants.
