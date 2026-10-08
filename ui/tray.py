import os
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


def _make_icon():
    img = Image.new('RGBA', (16,16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle((2,2,14,4), fill=(40,40,40,255))
    d.rectangle((2,6,10,8), fill=(60,60,60,255))
    d.rectangle((2,10,8,12), fill=(80,80,80,255))
    return img


class TrayApp:
    def __init__(self, on_toggle, on_settings, on_quit, get_enabled):
        self.on_toggle = on_toggle
        self.on_settings = on_settings
        self.on_quit = on_quit
        self.get_enabled = get_enabled
        self.icon = None

    def _build_menu(self):
        enabled = self.get_enabled()
        state = 'Disable' if enabled else 'Enable'
        return Menu(
            MenuItem(state, lambda: self._toggle()),
            MenuItem('Settings', lambda: self.on_settings()),
            MenuItem('Quit', lambda: self._quit()),
        )

    def _toggle(self):
        try:
            self.on_toggle()
        finally:
            try:
                self.icon.menu = self._build_menu()
                self.icon.update_menu()
            except Exception:
                pass

    def run(self):
        icon_img = _make_icon()
        self.icon = Icon('TypeFix', icon_img, 'TypeFix', self._build_menu())
        self.icon.run()

    def _quit(self):
        try:
            if self.icon:
                self.icon.stop()
        except Exception:
            pass
        self.on_quit()
