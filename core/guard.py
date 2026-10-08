import time


class Guard:
    def __init__(self, ttl: float = 1.5):
        self.ttl = ttl
        self._hwnd = None
        self._x = -10**12
        self._y = -10**12
        self._word_low = None
        self._t = 0

    def mark_protected(self, hwnd, x: int, y: int, wrong: str, right: str):
        self._hwnd = hwnd
        self._x = x
        self._y = y
        self._word_low = (right or wrong or '').lower()
        self._t = time.time()

    def is_protected_ctx(self, hwnd, x: int, y: int, word: str) -> bool:
        if not self._word_low or time.time() - self._t > self.ttl:
            return False
        dx = abs(x - self._x)
        dy = abs(y - self._y)
        if dx > 40 or dy > 20:
            return False
        if word and word.lower() == self._word_low:
            return True
        return False
