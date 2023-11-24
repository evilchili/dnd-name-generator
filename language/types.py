import inspect
import random
from collections import defaultdict
from typing import Union


class LanguageError(Exception):
    """
    Thrown when an error is encountered in language construction.
    """


class ImprobableTemplateError(Exception):
    """
    Thrown when too many successive attempts to create a word which passes all
    language rules fails.
    """


class WeightedSet:
    """
    A set in which members each have a weight, used for selecting at random.

    Usage:
        >>> ws = WeightedSet(('foo', 1.0), ('bar', 0.5))
        >>> ws.random()
        ('foo', 1.0)
    """

    def __init__(self, *weighted_members: tuple):
        self.members = []
        self.weights = []
        if weighted_members:
            self.members, self.weights = list(zip(*weighted_members))

    def random(self) -> str:
        return random.choices(self.members, self.weights)[0]

    def __add__(self, obj):
        ws = WeightedSet()
        ws.members = self.members + obj.members
        ws.weights = self.weights + obj.weights
        return ws

    def __str__(self):
        return f"{self.members}\n{self.weights}"


class Syllable:
    """
    One syllable of a word. Used to populate a SyllableSet.

    A syllable template is a string consisting of one or more grapheme types
    separated by a vertical pipe (|). Multiple template strings can be
    concatenated together with commas. When words are constructed, each
    syllable is populated with a random sequence chosen by
    Language.add_grapheme().

    A syllable template must contain at least one 'vowel'.

    Syllables can be multiplied by integers to produce repeated templates.

    Usage:
        # A syllable consisting of either a vowel or a consonant, followed by
        # a vowel, followed by either a vowel or consonant.
        >>> foo = Syllable(template='vowel|consonant,vowel,consonant|vowel')

        # Example multiplication
        >>> print(Syllable(template='vowel|consonant') * 3)
        vowel|consonant vowel|consonant vowel|consonant
    """

    def __init__(self, template: str = "vowel|consonant"):
        self.template = template
        self.validate()

    def validate(self):
        if "vowel" not in self.template:
            raise LanguageError(
                f"Invalid syllable template {self.template}!\n"
                "Syllables must have at least one vowel in the template."
            )

    def __mul__(self, count: int):
        return Syllable(template=",".join([self.template] * count))

    __rmul__ = __mul__

    def __str__(self):
        return self.template


class SyllableSet(WeightedSet):
    """
    A WeightedSet that selects random syllables.

    Usage:
        >>> word = SyllableSet(
                (Syllable('vowel'), 1.0),
                (Syllable('vowel|consonant') * 2, 1.0),
                (syllable('vowel|consonant,vowel|consonant') * 3, 0.75)
            )
        >>> word.random()
        vowel consonant consonant vowel
    """

    def random(self) -> iter:
        for syllable in random.choices(self.members, self.weights)[0].template.split(","):
            grapheme_template = random.choice(syllable.split("|"))
            yield grapheme_template.lower()


class Language:
    """
    A class representing a language.

    Usage:
        >>> Common = Language(
                name="common",
                vowels=WeightedSet(("a", 1.0), ("e", 1.0), ("i", 1.0), ...),
                consonants=WeightedSet(("b", 0.5), ("c", 0.5), ("d", 0.5), ...),
                prefixes=WeightedSet(("re", 0.5), ("de", 0.5), ("", 1.0), ...),
                suffixes=WeightedSet(("ed", 0.5), ("ing", 0.5), ("", 1.0), ...),
                syllables=SyllableSet(
                        (Syllable('consonant|vowel'), 1.0),
                        (Syllable('consonant|vowel') * 2, 0.75),
                        ...
                    ),
                rules=set(callable1, callable2, ...),
                minimum_grapheme_count=2,
            )
        >>> Common.word()
        reibing

    How Words Are Constructed:

        The main interface for callers is word(), which returns a
        randomly-generated word in the language according to the following
        algorithm:

        1. Choose a random syllable from the syllable set
        2. For each grapheme in the syllable
            3. Choose a random grapheme template
            4. Choose a random sequence from the language for that grapheme
            5. Validate the word against the language rules
        6. Repeat 1-5 until a valid word is generated
        7. Add a prefix and suffix, if they are defined

        The following graphemes are supported by default:
            - vowel
            - consonant
            - prefix
            - suffix

        When graphemes are chosen, the following rules are applied:
            - Every syllable must have at least one vowel
            - A syllable may never have three consecutive consonants

    How Words Are Validated:

        Once a word has been constructed by populating syllable templates, it is
        tested against one or more language rules.

        The default rules are defined in language.rules.default_rules; they are:
            - the word must contain at least one vowel
            - the word must not contain 3 or more contiguous english vowels
            - the word must not contain 3 or more contiguous english consonants
            - the word must not consist of just one vowel, repeated

        Since it is possible to craft Syllables resulting in grapheme
        selections that rarely or never yield valid words, or rules that
        reject every word, an ImprobableTemplateError will be thrown if
        10 successive attempts to create a valid word fail.

    Extending Languages:

        Graphemes are populated by means of callbacks which select a member
        of the associated weighted set at random. Graphemes can be any string,
        so long as the Language class has a matching callback.

        To add support for a new grapheme type, define a method on your
        Language class called get_grapheme_TYPE, where TYPE is the string
        used in your Syllable templates. Examine test cases in test_types.py
        for examples.
    """

    def __init__(
        self,
        name: str,
        vowels: WeightedSet,
        consonants: WeightedSet,
        prefixes: WeightedSet,
        suffixes: WeightedSet,
        syllables: SyllableSet,
        rules: set = set(),
        minimum_grapheme_count: int = 1,
    ):
        """
        Args:
            name                   - friendly name for the language
            vowels                 - the weighted set of vowel graphemes
            consonants             - the weighted set of consonant graphemes
            prefixes               - the weighted set of prefix graphemes
            suffixes               - the weighted set of suffix graphemes
            rules                  - a set of rules callbacks; see above.
            minimum_grapheme_count - the minimum number of graphemes in each word
        """
        self.name = name
        self.vowels = vowels
        self.consonants = consonants
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.rules = rules
        self.syllables = syllables
        self.minimum_grapheme_count = minimum_grapheme_count
        self.validate_syllable_set()

        self.handlers = dict([(n, v) for (n, v) in inspect.getmembers(self, inspect.ismethod) if n.startswith("get_")])

    def validate(self, word: str) -> bool:
        """
        Returns true if the given word is possible in the current language.
        """
        if not word:
            return False
        for rule in self.rules:
            if not rule(self, word):
                return False
        return True

    def validate_syllable_set(self):
        for syllable in self.syllables.members:
            if len(syllable.template.split(",")) < self.minimum_grapheme_count:
                raise ImprobableTemplateError(
                    f"Syllable {syllable} does not define enough graphemes ({self.minimum_grapheme_count} required)."
                )

    def validate_graphemes(self, graphemes: list) -> bool:
        if len(graphemes) < self.minimum_grapheme_count:
            return False

        last = ""
        count = 0
        for g in graphemes:
            if g == last:
                count += 1
                if count == 3:
                    return False
            else:
                count = 1
            last = g
        return True

    def word(self, count: int = 1) -> list:
        """
        Yields words composed of randomized phonemes built from a random word template.
        """
        words = []
        for _ in range(count):
            random_word = ""
            attempts = 0
            while not self.validate(random_word):
                if attempts == 10:
                    raise ImprobableTemplateError(
                        f"Exhausted all attempts to create a valid word. Last attempt: {random_word}. "
                        "If you're getting this a lot, try enabling debugging to see what rules are failing."
                    )
                graphemes = []
                random_word = ""
                while not self.validate_graphemes(graphemes):
                    graphemes = list(self.syllables.random())
                for grapheme in graphemes:
                    random_word = self.add_grapheme(random_word, grapheme)
                attempts += 1
            if self.prefixes:
                random_word = self.get_grapheme_prefix() + random_word
            if self.suffixes:
                random_word = random_word + self.get_grapheme_suffix()
            words.append(random_word)
        return words

    def add_grapheme(self, word: str, template: str) -> str:
        """
        Returns a random grapheme of a supported type. The class must support a method of the name:
            get_grapheme_{template}
        """
        template = template.lower()
        try:
            return word + self.handlers[f"get_grapheme_{template}"]()
        except KeyError:
            raise NotImplementedError(
                f"No handler found for grapheme template '{template}'. "
                f"Do you need to define get_grapheme_{template}()?\n"
                "Supported handlers: " + self.handlers.keys
            )

    def get_grapheme_consonant(self) -> str:
        return self.consonants.random()

    def get_grapheme_vowel(self) -> str:
        return self.vowels.random()

    def get_grapheme_prefix(self) -> str:
        return self.prefixes.random()

    def get_grapheme_suffix(self) -> str:
        return self.suffixes.random()

    def text(self, count: int = 25) -> str:
        phrases = []
        phrase = []
        for word in self.word(count):
            phrase.append(str(word))
            if len(phrase) >= random.randint(1, 12):
                phrases.append(" ".join(phrase))
                phrase = []
        if phrase:
            phrases.append(" ".join(phrase))

        paragraph = phrases[0].capitalize()
        for phrase in phrases[1:]:
            if random.choice([0, 0, 1]):
                paragraph = paragraph + random.choice("?!.") + " " + phrase.capitalize()
            else:
                paragraph = paragraph + ", " + phrase
        paragraph = paragraph + random.choice("?!.")
        return paragraph

    def copy(self):
        return self.__class__(
            name=self.name,
            vowels=self.vowels,
            consonants=self.consonants,
            prefixes=self.prefixes,
            suffixes=self.suffixes,
            rules=self.rules,
            syllables=self.syllables,
            minimum_grapheme_count=self.minimum_grapheme_count,
        )

    def __str__(self) -> str:
        return self.word()[0]


NameSet = SyllableSet


class Name(defaultdict):
    def __str__(self):
        return self["fullname"][0]


class NameTemplate(Syllable):
    def validate(self):
        pass


class NameGenerator:
    def __init__(
        self,
        language: Language,
        templates: NameSet,
        syllables: Union[SyllableSet, None] = None,
        names: Union[WeightedSet, None] = None,
        surnames: Union[WeightedSet, None] = None,
        nicknames: Union[WeightedSet, None] = None,
        adjectives: Union[WeightedSet, None] = None,
        titles: Union[WeightedSet, None] = None,
        counts: Union[WeightedSet, None] = None,
        affixes: Union[WeightedSet, None] = None,
        suffixes: Union[WeightedSet, None] = None,
    ):
        self.language = language.copy()
        if syllables:
            self.language.syllables = syllables
        self.templates = templates
        self._names = names
        self._surnames = surnames
        self._nicknames = nicknames
        self._adjectives = adjectives
        self._titles = titles
        self._counts = counts
        self._suffixes = suffixes
        self._affixes = affixes

        self.handlers = dict([(n, v) for (n, v) in inspect.getmembers(self, inspect.ismethod) if n.startswith("get_")])

    def name(self, count: int = 1) -> list:
        """
        Generate Name instances.
        """
        names = []
        for _ in range(count):
            name = Name(list)
            fullname = []
            for part in self.templates.random():
                thisname = self.add_part(part).strip()
                if not thisname:
                    continue
                name[part].append(thisname)
                fullname.append(thisname)
            name["fullname"] = " ".join(fullname)
            names.append(name)
        return names

    def add_part(self, template: str) -> str:
        template = template.lower()
        try:
            return self.handlers[f"get_{template}"]()
        except KeyError:
            raise NotImplementedError(
                f"No handler found for name template '{template}' on class {self.__class__.__name__}. "
                f"Do you need to define get_{template}()?\nSupported Handlers: "
                + ",".join(n for n in dir(self) if n.startswith("get_"))
            )

    def get_name(self) -> str:
        name = (self._names.random() if self._names else self.language.word())[0]
        return name.title()

    def get_surname(self) -> str:
        name = (self._surnames.random() if self._surnames else self.language.word())[0]
        if self._suffixes:
            name = name + self._suffixes.random()
        if len(name) == 1:
            name = f"{name}."
        return name.title()

    def get_adjective(self) -> str:
        return (self._adjectives.random() if self._adjectives else "").title()

    def get_affix(self) -> str:
        return self._affixes.random() if self._affixes else ""

    def get_title(self) -> str:
        return (self._titles.random() if self._titles else "").title()

    def get_the(self) -> str:
        return "the"

    def get_count(self) -> str:
        return self._counts.random() if self._counts else ""

    def get_nickname(self) -> str:
        name = (self._nicknames.random() if self._nicknames else "").title()
        if name:
            return '"' + name + '"'
        return ""

    def get_initial(self) -> str:
        return

    def __str__(self) -> str:
        return self.name()[0]["fullname"]


def equal_weights(terms: list, weight: float = 1.0, blank: bool = True) -> WeightedSet:
    ws = WeightedSet(*[(term, weight) for term in terms])
    if blank:
        ws = WeightedSet(("", 1.0)) + ws
    return ws
