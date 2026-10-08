try:
    import win32gui
    import win32api
except Exception:
    win32gui = None
    win32api = None

import ctypes
from ctypes import wintypes


class WinUtil:
    def get_foreground_hwnd(self):
        try:
            if win32gui:
                return win32gui.GetForegroundWindow()
        except Exception:
            pass
        return None

    def get_caret_rect(self):
        try:
            hwnd = self.get_foreground_hwnd()
            if hwnd is None:
                return None
            if ctypes.windll.user32:
                class GUITHREADINFO(ctypes.Structure):
                    _fields_ = [
                        ('cbSize', wintypes.DWORD),
                        ('flags', wintypes.DWORD),
                        ('hwndActive', wintypes.HWND),
                        ('hwndFocus', wintypes.HWND),
                        ('hwndCapture', wintypes.HWND),
                        ('hwndMenuOwner', wintypes.HWND),
                        ('hwndMoveSize', wintypes.HWND),
                        ('hwndCaret', wintypes.HWND),
                        ('rcCaret', wintypes.RECT),
                    ]
                gti = GUITHREADINFO()
                gti.cbSize = ctypes.sizeof(GUITHREADINFO)
                user32 = ctypes.windll.user32
                if user32.GetGUIThreadInfo(0, ctypes.byref(gti)):
                    r = gti.rcCaret
                    x, y, w, h = r.left, r.top, r.right-r.left, r.bottom-r.top
                    try:
                        pt = wintypes.POINT(x,y)
                        hc = gti.hwndCaret or hwnd
                        user32.ClientToScreen(hc, ctypes.byref(pt))
                        x,y = pt.x,pt.y
                    except Exception:
                        pass
                    return (x,y,w,h)
            if win32gui and win32api:
                try:
                    _, x, y = win32gui.GetCaretPos()
                    return (x,y,2,16)
                except Exception:
                    pass
        except Exception:
            pass
        return None
