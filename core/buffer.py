class Buffer:
    def __init__(self):
        self._chars = []

    @property
    def current_word(self) -> str:
        return ''.join(self._chars)

    def current_word_before_space(self) -> str:
        return self.current_word

    def type_char(self, c: str):
        self._chars.append(c)

    def backspace(self, is_delete: bool = False):
        if self._chars:
            self._chars.pop()

    def clear(self):
        self._chars.clear()

    def commit(self):
        self._chars.clear()
