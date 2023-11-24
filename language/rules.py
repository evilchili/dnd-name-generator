import logging
import re

from language.types import Language

logger = logging.getLogger()


def too_many_vowels(language: Language, word: str) -> bool:
    found = re.compile(r"[aeiou]{3}").findall(word)
    if found == []:
        return True
    logger.debug(f"{word} has too many contiguous vowels: {found}")
    return False


def too_many_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"[bcdfghjklmnpqrstvwxz]{3}").findall(word)
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


default_rules = {must_have_a_vowel, too_many_vowels, too_many_consonants, cannot_have_just_repeated_vowels}
