import logging
import re

from language.rules import default_rules
from language.types import Language

logger = logging.getLogger("orcish-rules")


def cannot_start_with_repeated_consonants(language: Language, word: str) -> bool:
    found = re.compile(r"(^[bcdfghklmnpqrstvwxz]{3})").search(word)
    if not found:
        return True

    first, second, third = found.group(1)
    if first == second == third:
        logger.debug(f"{word} starts with a repeated consonant.")
        return False

    return True


rules = default_rules
rules.add(cannot_start_with_repeated_consonants)
