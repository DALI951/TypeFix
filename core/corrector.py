import os
from typing import Optional

from symspellpy import SymSpell, Verbosity

from utils.textutil import should_ignore_word


class Corrector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.sym = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        self._load_dict()
        self.reload(cfg)

    def _load_dict(self):
        base = os.path.dirname(os.path.dirname(__file__))
        p = os.path.join(base, 'data', 'en_freq.txt')
        try:
            if os.path.exists(p):
                self.sym.load_dictionary(p, term_index=0, count_index=1, encoding='utf-8')
        except Exception:
            pass

    def reload(self, cfg):
        self.cfg = cfg

    def should_ignore(self, word: str) -> bool:
        if should_ignore_word(word):
            return True
        ignore_list = self.cfg.data.get('ignore_list') or []
        wl = word.lower()
        if wl in [x.lower() for x in ignore_list]:
            return True
        return False

    def is_misspelled(self, word: str) -> bool:
        if self.should_ignore(word):
            return False
        wl = word.lower()
        suggestions = self.sym.lookup(wl, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            return False
        return True

    def suggest(self, word: str, n: int = 1) -> Optional[str]:
        if not word:
            return word
        wl = word.lower()
        learned = self.cfg.data.get('learned') or {}
        custom = self.cfg.data.get('custom_map') or {}
        if wl in learned and learned[wl]:
            cand = learned[wl]
            return cand.capitalize() if word and word[0].isupper() else cand
        if wl in custom and custom[wl]:
            cand = custom[wl]
            return cand.capitalize() if word and word[0].isupper() else cand
        suggestions = self.sym.lookup(wl, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=False)
        for s in suggestions[:n]:
            cand = s.term
            if cand:
                return cand.capitalize() if word and word[0].isupper() else cand
        return word
