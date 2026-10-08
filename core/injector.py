import time

try:
    import keyboard
except Exception:
    keyboard = None

try:
    import pyautogui
except Exception:
    pyautogui = None

import ctypes
from ctypes import wintypes


class _KI(ctypes.Structure):
    _fields_ = [('wVk', wintypes.WORD), ('wScan', wintypes.WORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_size_t)]


class _MI(ctypes.Structure):
    _fields_ = [('dx', wintypes.LONG), ('dy', wintypes.LONG), ('mouseData', wintypes.DWORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_size_t)]


class _U(ctypes.Union):
    _fields_ = [('ki', _KI), ('mi', _MI)]


class _IN(ctypes.Structure):
    _anonymous_ = ('u',)
    _fields_ = [('type', wintypes.DWORD), ('u', _U)]


try:
    _SendInput = ctypes.windll.user32.SendInput
except Exception:
    _SendInput = None


def _k(vk=0, scan=0, flags=0):
    return _IN(1, _U(ki=_KI(vk, scan, flags, 0, 0)))


def _inject(back, text, tail):
    for vk in (0x10, 0x11, 0x12):
        if ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000:
            return False
    ev = []
    for _ in range(tail):
        ev += [_k(0x25, 0, 1), _k(0x25, 0, 3)]
    for _ in range(back):
        ev += [_k(0x08), _k(0x08, 0, 2)]
    for ch in text:
        ev += [_k(0, ord(ch), 4), _k(0, ord(ch), 6)]
    for _ in range(tail):
        ev += [_k(0x27, 0, 1), _k(0x27, 0, 3)]
    arr = (_IN * len(ev))(*ev)
    _SendInput(len(ev), arr, ctypes.sizeof(_IN))
    return True


class Injector:
    def replace_word(self, wrong_len: int, correct: str, tail: int = 0):
        try:
            if wrong_len < 0:
                wrong_len = 0
            if _SendInput is not None:
                return _inject(wrong_len, correct, tail)
            if keyboard is not None:
                for _ in range(wrong_len):
                    keyboard.press_and_release('backspace')
                    time.sleep(0.0003)
                keyboard.write(correct)
                return
            if pyautogui is not None:
                for _ in range(wrong_len):
                    pyautogui.press('backspace')
                    time.sleep(0.0003)
                pyautogui.typewrite(correct)
                return
        except Exception:
            pass
