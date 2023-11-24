import logging
import re

from language.types import Language

logger = logging.getLogger("elvish-rules")

permitted_starting_clusters = [
    "ch",
    "cl",
    "cr",
    "cw",
    "cy",
    "dh",
    "dj",
    "dr",
    "dw",
    "dy",
    "fl",
    "fn",
    "fr",
    "fw",
    "fy",
    "gl",
    "ll",
    "ly",
    "ml",
    "mw",
    "my",
    "ny",
    "rh",
    "ry",
    "sh",
    "sl",
    "sm",
    "sn",
    "st",
    "sv",
    "sw",
    "sy",
    "th",
    "tr",
    "tw",
    "ty",
    "vy",
    "wh",
    "wr",
    "wy",
    "yh",
]


def cannot_start_with_two_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"(^[bcdfghklmnpqrstvwxz]{2})").search(word)
    if not found:
        return True

    first, second = found.group(1)
    if first == second and first != "l":
        logger.debug(f"{word} starts with a repeated consonant.")
        return False

    if found.group(1) not in permitted_starting_clusters:
        logger.debug("f{word} cannot start with {first}{second}")
        return False
    return True


def too_many_vowels(language: Language, word: str) -> bool:
    found = re.compile(r"[" + "".join(language.vowels.members) + "]{4}").findall(word)
    if found == []:
        return True
    logger.debug(f"{word} has too many contiguous vowels: {found}")
    return False


def too_many_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"[bcdfghklmnprstvw]{3}").findall(word)
    if found == []:
        return True
    logger.debug(f"{word} has too many contiguous consonants: {found}")
    return False


def cannot_have_just_repeated_vowels(language: Language, word: str) -> bool:
    if len(word) == 1:
        return True
    uniq = {letter for letter in word}
    if len(uniq) > 1:
        return True
    logger.debug(f"{word} consists of only one repeated letter.")
    return False


def must_have_a_vowel(language: Language, word: str) -> bool:
    for vowel in language.vowels.members:
        if vowel in word:
            return True
    logger.debug(f"{word} does not contain a vowel.")
    return False


rules = {
    must_have_a_vowel,
    too_many_vowels,
    too_many_consonants,
    cannot_have_just_repeated_vowels,
    cannot_start_with_two_consonants,
}
