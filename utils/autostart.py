import os
import sys

try:
    import winreg
except Exception:
    winreg = None


def _exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py'))


def set_autostart(enable: bool):
    if winreg is None:
        return
    key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as k:
            if enable:
                p = _exe_path()
                if getattr(sys, 'frozen', False):
                    val = f'"{p}"'
                else:
                    py = sys.executable
                    val = f'"{py}" "{p}"'
                winreg.SetValueEx(k, 'TypeFix', 0, winreg.REG_SZ, val)
            else:
                try:
                    winreg.DeleteValue(k, 'TypeFix')
                except FileNotFoundError:
                    pass
    except Exception:
        pass
