import threading
import time
import pythoncom

from core.buffer import Buffer
from core.corrector import Corrector
from core.guard import Guard
from core.hook import KeyHook
from core.injector import Injector
from overlay.underline import UnderlineOverlay
from ui.tray import TrayApp
from utils.config import Config
from utils.winutil import WinUtil


class App:
    def __init__(self):
        self.cfg = Config()
        self.cfg.load()
        self.corrector = Corrector(self.cfg)
        self.guard = Guard()
        self.buffer = Buffer()
        self.injector = Injector()
        self.overlay = UnderlineOverlay(self.cfg)
        self.winutil = WinUtil()
        self.running = True
        self._last_check = 0
        self._check_throttle = 0.07
        self.hook = KeyHook(self.on_key)
        self.tray = TrayApp(
            on_toggle=self.toggle_enabled,
            on_settings=self.open_settings,
            on_quit=self.quit,
            get_enabled=lambda: self.cfg.data.get('enabled', True),
        )

    def toggle_enabled(self):
        self.cfg.data['enabled'] = not self.cfg.data.get('enabled', True)
        self.cfg.save()
        self.overlay.hide()

    def open_settings(self):
        try:
            from ui.settings import SettingsWindow
            SettingsWindow(self.cfg, on_changed=self._on_cfg_changed)
        except Exception:
            pass

    def _on_cfg_changed(self):
        self.corrector.reload(self.cfg)
        self.overlay.hide()

    def quit(self):
        self.running = False
        try:
            self.overlay.destroy()
        except Exception:
            pass
        try:
            self.hook.stop()
        except Exception:
            pass

    def on_key(self, key_name: str, is_down: bool):
        if not is_down:
            return
        if not self.cfg.data.get('enabled', True):
            return
        k = (key_name or '').lower()
        if k == 'space':
            self._handle_space()
            return
        if k in ('backspace', 'delete'):
            self.buffer.backspace(k == 'delete')
            self._update_overlay()
            return
        if k in ('left', 'right', 'up', 'down', 'home', 'end', 'page_up', 'page_down', 'insert', 'enter', 'tab', 'esc', 'escape'):
            self.buffer.clear()
            self.overlay.hide()
            return
        if len(k) == 1 and k.isprintable():
            self.buffer.type_char(k)
            self._update_overlay()
            return
        if k.startswith('shift') or k.startswith('ctrl') or k.startswith('alt') or k.startswith('win'):
            return
        self.buffer.clear()
        self.overlay.hide()

    def _update_overlay(self):
        now = time.time()
        if now - self._last_check < self._check_throttle:
            return
        self._last_check = now
        if not self.cfg.data.get('underline_wrong', True):
            self.overlay.hide()
            return
        word = self.buffer.current_word
        if not word:
            self.overlay.hide()
            return
        caret = self.winutil.get_caret_rect()
        if not caret:
            return
        hwnd = self.winutil.get_foreground_hwnd()
        if self.guard.is_protected_ctx(hwnd, caret[0], caret[1], word):
            self.overlay.hide()
            return
        if self.corrector.is_misspelled(word):
            self.overlay.show(caret)
        else:
            self.overlay.hide()

    def _handle_space(self):
        if not self.cfg.data.get('correct_on_space', True):
            self.buffer.commit()
            self.overlay.hide()
            return
        word = self.buffer.current_word_before_space()
        self.buffer.commit()
        if not word:
            self.overlay.hide()
            return
        hwnd = self.winutil.get_foreground_hwnd()
        caret = self.winutil.get_caret_rect() or (0,0,0,0)
        if self.guard.is_protected_ctx(hwnd, caret[0], caret[1], word):
            self.overlay.hide()
            return
        if not self.corrector.should_ignore(word) and self.corrector.is_misspelled(word):
            sugg = self.corrector.suggest(word, 1)
            if sugg and sugg.lower() != word.lower():
                try:
                    self.injector.replace_word(len(word), sugg)
                except Exception:
                    pass
                self.guard.mark_protected(hwnd, caret[0], caret[1], word, sugg)
                self.cfg.data.setdefault('learned', {})[word.lower()] = sugg
                self.cfg.save()
                self.corrector.reload(self.cfg)
                self.overlay.hide()
                return
        self.overlay.hide()

    def run(self):
        try:
            self.hook.start()
        except Exception:
            pass
        try:
            self.tray.run()
        except Exception:
            pass


def main():
    try:
        pythoncom.CoInitialize()
    except Exception:
        pass
    app = App()
    app.run()


if __name__ == '__main__':
    main()
