import time

try:
    import keyboard
except Exception:
    keyboard = None

try:
    import pyautogui
except Exception:
    pyautogui = None


class Injector:
    def replace_word(self, wrong_len: int, correct: str):
        try:
            if wrong_len < 0:
                wrong_len = 0
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
