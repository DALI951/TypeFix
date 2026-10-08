import threading

try:
    import keyboard
except Exception:
    keyboard = None


class KeyHook:
    def __init__(self, callback):
        self.callback = callback
        self._running = False

    def _handler(self, event):
        try:
            name = event.name or ''
            is_down = event.event_type == keyboard.KEY_DOWN
            self.callback(name, is_down)
        except Exception:
            import traceback, os; open(os.path.expanduser('~/typefix_err.log'), 'a').write(traceback.format_exc())

    def start(self):
        if self._running or keyboard is None:
            return
        self._running = True
        keyboard.hook(self._handler)
        t = threading.Thread(target=keyboard.wait, daemon=True)
        t.start()

    def stop(self):
        self._running = False
        try:
            keyboard.unhook_all()
        except Exception:
            pass
