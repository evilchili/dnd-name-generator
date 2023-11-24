import logging
import re

from language.rules import default_rules
from language.types import Language

logger = logging.getLogger()

valid_consonant_sequences = [
    "cc",
    "ht",
    "kd",
    "kl",
    "km",
    "kp",
    "kt",
    "kv",
    "kw",
    "ky",
    "lc",
    "ld",
    "lf",
    "ll",
    "lm",
    "lp",
    "lt",
    "lv",
    "lw",
    "ly",
    "mb",
    "mm",
    "mp",
    "my",
    "nc",
    "nd",
    "ng",
    "nn",
    "nt",
    "nw",
    "ny",
    "ps",
    "pt",
    "rc",
    "rd",
    "rm",
    "rn",
    "rp",
    "rr",
    "rs",
    "rt",
    "rw",
    "ry",
    "sc",
    "ss",
    "ts",
    "tt",
    "th",
    "tw",
    "ty",
]


def valid_sequences(language: Language, word: str) -> bool:
    found = re.compile(r"([bcdfghjklmnpqrstvwxz]{2})").findall(word)
    if not found:
        return True

    invalid = [seq for seq in found if seq not in valid_consonant_sequences]
    if invalid:
        logger.debug(f"{word} contains invalid consonant sequences: {invalid}")
        return False
    return True


def too_many_vowels(language: Language, word: str) -> bool:
    found = re.compile(r"[" + "".join(language.vowels.members) + r"]{3}").findall(word)
    if found == []:
        return True
    logger.debug(f"{word} has too many contiguous vowels: {found}")
    return False


rules = default_rules.union(
    {
        valid_sequences,
        too_many_vowels,
    }
)
