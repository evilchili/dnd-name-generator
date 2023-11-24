# D&D Name and Language Generator

This package is a fantasy language generator. By defining a number of characteristics about your imagined language -- the graphemes, their relative frequency distributions, the construction of syllables, and so on -- you can generate random but internally consistent gibberish that feels distinct, evocative, and appropriate to your setting.

## Usage

The `fanlang` command-line utility supports three commands:

* **names**: generate names 
* **text**: generate a paragraph of text 
* **list**: list the supported language in the current language pack

### Examples:

```
% fanlang --language=dwarvish names --count 5
Tiny Châ Pothesadottyr
Khâkhu Zhûdothir
Quiet Ke Vêdothir
Cû Tozhon
Big Pâ Thadottyr
```

```
% fanlang --language=dwarvish text
Cû ne do tho khâ tasha, vê wûva lû, ku phu thâ thê, tûko kê, pevo kâ têtetv zha 
pataso keks khate? Fâ zhû shû yf pho pa me. Dupha dê thê khâ! Shikm tu! Cê 
sâdêto. Dê yo nâ topho, my sû pida phe, vi phûtw châcho, po sotê?
```

```
% fanlang list
Abyssal                                                                         
Celestial                                                                       
Common                                                                          
Draconic                                                                        
Dwarvish                                                                        
Elvish                                                                          
Gnomish                                                                         
Halfling                                                                        
Infernal                                                                        
Lizardfolk                                                                      
Orcish                                                                          
Undercommon
```

## Language Packs

A *Language Pack* is a python package that defines one or more language modules. The default language pack includes a number of D&D languages with rules built according to the conventions established by my D&D group over several years of play in our homebrew setting.

The default language pack is [language.languages](language/languages/); each submodule contains a README that describes the basic characteristics of the language, along with examples.

### Using Your Own Language Pack

You can override `fanlang`'s default language pack by specifying the `FANLANG_LANGUAGE_PACK` environment variable:

```
# Create your ancient_elvish module in campaign/language_pack/ancient_elvish
% FANLANG_LANGUAGE_PACK=campaign.language_pack fanlang list
Ancient Elvish
```

### Setting the Default Language

'common' is the default language module. You can override this by setting the `FANLANG_DEFAULT_LANGUAGE` environment variable:

```
% FANLANG_DEFAULT_LANGUAGE=gnomish fanlang names --count=1
Jey Lea
```

You can read about creating custom language packs below.


## Library Quick Start

You can load all supported languages in a language pack using `language.load_langauge_pack()`:

```
>>> import language
>>> language_pack, supported_languages = language.load_language_pack()
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

You can also load individual languages directly:

```
>>> from language.languages import common
>>> common.Language.word(2)
['apsoo', 'nirtoet']
>>> str(common.Name)
"Quiet" Gushi Murk Lirpusome
```

## Defining a New Language Pack

Language packs are python packages with the following structure:

```
language_pack:
  __init__.py
  language_name:
    __init__.py
    README.md
    base.py
    names.py
    rules.py
  ...
```

### Language Modules

A language consists of several submodules:

* `base.py`, which contains grapheme definitions and a `Language` subclass;
* `names.py`, which defines the `NameGenerator` subclasses; and
* `rules.py`, which is optional, and defines the rules all words in the language must follow.

Read on for a discussion of each of these components.

## Language Generators

Let's look at a simple example, the Gnomish language. Here's the `Language`
subclass defined in `base.py`:

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

### Defining Graphemes

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

### Defining Syllables

A syllable is a collection of graphemes, including at least one vowel. When we
create words, we select a random syllable template from a `SyllableSet`, which
is just a `WeightedSet` whose members are `Syllable` instances. Each `Syllable`
declares a `template`, and like graphemes, has a weight associated with it that
will make it more or less likely to be chosen for a word.

A syllable's template consists of a comma-separated string of grapheme names.
In Gnomish, we have two possible syllable templates, `consonant,vowel,vowel`
and the shorter `consonant,vowel`, which will be selected one third as often.

Templates also support randomly-selected graphemes by joining two or more
grapheme types with a vertical bar, for example `vowel|consonant` would choose
one or the other; `vowel|consonant,vowel` would result in a vowel or
a consonant followed by a vowel.

### How Words Are Constructed:

The main interface for callers is `word()`, which returns a randomly-generated
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

### A More Complex Example

[The Common language](language/languages/common/base.py) is a more complex definition, with language-specific prefixes, suffixes, vowels, and consonants, and many possible syllables. This results in highly-varied text.

## Rules

Rules are a set of callables that accept a language instance and a word. The callable returns `True` if the word passes some test, and `False` otherwise. Every randomly-generated word must pass all defined rules for the language, or it is rejected.

[The language.rules module(language/rules.py) contains a number of useful rules that are applied by default to most languages, mostly used to aid readability and generate words that are pronouncable. Here's a simple example:

```
def too_many_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"[bcdfghjklmnpqrstvwxz]{3}").findall(word)
    if found == []:
        return True
    logger.debug(f"{word} has too many contiguous consonants: {found}")
    return False
```

This rule ensures that a word does not contain more than 3 english consonants in a row.

### Defining Language-Specific Rules

Rules are passed as a set of callables to the `Language` constructor, so they can be anything you want, defined anywhere you want. By convention, language packs use a separate `rules` module when building custom rule sets.

## Name Generators

Name generators are similar to Language generators, but with a few key differences. Here is a simple example, also from the Gnomish language:

```
from language import types
from language.languages.gnomish import Language

Name = types.NameGenerator(
    language=Language,
    templates=types.NameSet(
        (types.NameTemplate("name,surname"), 1.0),
    ),
)
NobleName = Name
```

In Gnomish, names are straightforward, consisting of a name and a surname, and there is no distinction between regular names and the names of the nobility. By contrast, [Elvish names are complex](language/languages/elvish/names.py), consisting of multiple distinct parts, including place names, affixes, and separate rules for common and noble name construction.


### Defining Names

Name Generators are defined with a Language, and one or more `NameSet` templates. `NameSets` are equivalent to `SyllableSets`, but instead of creating templates for the construction of syllables from sequences of graphemes, they define sequences of parts of names -- **names**, **surnames**, **titles**, **nicknames**, and so on. They follow the same semantics as `Syllables`, allowing for a large variety of potential names.

By default, both **names** and **surnames** are generated automatically by calling `NameGenerator.language.word()`. Thus, the simplest name generator will simply follow all the rules of the language itself and generate one or more random words. You can override multiple aspects of a language's rules for word generation by passing `NameGenerator` additional arguments. For example, here is a generator for the names of locations in the Elvish language:

```
from language import types, defaults
from language.languages.elvish import Language

PlaceName = types.NameGenerator(
    language=Language,
    syllables=types.SyllableSet(
        (types.Syllable(template="vowel,vowel|consonant,vowel|consonant"), 1.0),
        (types.Syllable(template="consonant,vowel|consonant,vowel|consonant"), 0.3),
    ),
    templates=types.NameSet(
        (types.NameTemplate("affix,name"), 1.0),
    ),
    affixes=types.WeightedSet(("el", 1.0)),
    adjectives=defaults.adjectives,
)
```

Note how we declare new `syllables`, `affixes`, and `adjectives`, which will replace the `Language`'s default behaviours. 

#### Subclassing

Sometimes we need even more control than providing new syllable sets and weighted sets for graphemes. Subclassing `NameGenerator` gives you significant control over how names are constructed. For example, Elvish surnames are based on Elvish place names; to accomplish this, we subclass `NameGenerator` and override the method used to generate surnames:

```
class ElvishNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=Language,
            syllables=Language.syllables,
            templates=types.NameSet(
                (types.NameTemplate("name,affix,surname"), 1.0),
            ),
            affixes=types.equal_weights(["am", "an", "al", "um"], weight=1.0, blank=False),
            adjectives=defaults.adjectives,
            titles=defaults.titles,
            suffixes=suffixes,
        )
        self.place_generator = PlaceName

    def get_surname(self) -> str:
        return self.place_generator.name()[0]["name"][0]
```
