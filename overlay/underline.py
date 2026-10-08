import tkinter as tk
import time


class UnderlineOverlay:
    def __init__(self, cfg):
        self.cfg = cfg
        self.root = None
        self._visible = False
        self._last_update = 0
        self._throttle = 0.07
        self._create()

    def _create(self):
        try:
            self.root = tk.Tk()
            self.root.title('TypeFixOverlay')
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            self.root.attributes('-disabled', True)
            self.root.configure(bg='black')
            self._canvas = tk.Canvas(self.root, width=1, height=2, bg='black', highlightthickness=0)
            self._canvas.pack()
            self.root.withdraw()
        except Exception:
            self.root = None

    def show(self, caret_rect):
        now = time.time()
        if now - self._last_update < self._throttle:
            pass
        self._last_update = now
        if self.root is None:
            return
        try:
            x, y, w, h = caret_rect
            line_w = max(8, int(w * 0.9)) if w > 0 else 20
            line_h = 2
            self._canvas.config(width=line_w, height=line_h)
            self.root.geometry(f'{line_w}x{line_h}+{x}+{y+2}')
            if not self._visible:
                self.root.deiconify()
                self._visible = True
            self.root.update_idletasks()
        except Exception:
            pass

    def hide(self):
        if not self._visible or self.root is None:
            return
        try:
            self.root.withdraw()
            self._visible = False
        except Exception:
            pass

    def destroy(self):
        try:
            if self.root:
                self.root.destroy()
        except Exception:
            pass
