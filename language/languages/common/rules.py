import logging
import re

from language.rules import default_rules
from language.types import Language

logger = logging.getLogger()

permitted_starting_clusters = [
    "bh",
    "bl",
    "br",
    "bw",
    "by",
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
    "gh",
    "gl",
    "gn",
    "gr",
    "gw",
    "gy",
    "hy",
    "jh",
    "jy",
    "kh",
    "kl",
    "kr",
    "kw",
    "ky",
    "ll",
    "ly",
    "mw",
    "my",
    "ny",
    "ph",
    "pl",
    "pn",
    "pr",
    "pw",
    "py",
    "rh",
    "ry",
    "sb",
    "sc",
    "sd",
    "sf",
    "sg",
    "sh",
    "sj",
    "sk",
    "sl",
    "sm",
    "sn",
    "sp",
    "sr",
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
    "xh",
    "xy",
    "yh",
    "zb",
    "zc",
    "zd",
    "zh",
    "zl",
    "zm",
    "zn",
    "zr",
    "zw",
    "zy",
]


def cannot_start_with_two_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"(^[bcdfghjklmnpqrstvwxz]{2})").search(word)
    if not found:
        return True
    first, second = found.group(1)

    if first == second:
        logger.debug(f"{word} starts with a repeated consonant.")
        return False

    return found in permitted_starting_clusters


rules = default_rules.union(
    {
        cannot_start_with_two_consonants,
    }
)
