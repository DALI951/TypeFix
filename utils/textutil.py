import re


EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
URL_RE = re.compile(r"(https?://|www\.)", re.IGNORECASE)
NUMBER_RE = re.compile(r"^\d+([.,]\d+)*$")
MIXED_NUM_LET_RE = re.compile(r".*\d.*")


def should_ignore_word(word: str) -> bool:
    if not word:
        return True
    w = word
    if len(w) <= 1:
        return True
    if w.isupper():
        return True
    if EMAIL_RE.search(w):
        return True
    if URL_RE.search(w):
        return True
    if NUMBER_RE.match(w):
        return True
    if MIXED_NUM_LET_RE.match(w) and not w.isalpha():
        return True
    for ch in w:
        if ch.isalpha() is False and ch not in ("'", '-', '_'):
            return True
    return False
