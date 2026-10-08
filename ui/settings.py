import tkinter as tk
from tkinter import ttk, messagebox


class SettingsWindow:
    def __init__(self, cfg, on_changed=None):
        self.cfg = cfg
        self.on_changed = on_changed
        self.root = tk.Tk()
        self.root.title('TypeFix Settings')
        self.root.geometry('360x360')
        self.root.resizable(False, False)
        self._vars = {}
        self._build()
        self.root.mainloop()

    def _var(self, key, default=True):
        if key not in self._vars:
            val = self.cfg.data.get(key, default)
            v = tk.BooleanVar(value=bool(val))
            self._vars[key] = v
        return self._vars[key]

    def _build(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.grid(sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        row = 0
        ttk.Label(frm, text='General').grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Enable TypeFix', variable=self._var('enabled', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Auto-start with Windows', variable=self._var('autostart', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Underline misspelled while typing', variable=self._var('underline_wrong', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Correct on Space (silent)', variable=self._var('correct_on_space', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Show Fix button near underline', variable=self._var('show_fix_button', False)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Ignore ALL-CAPS', variable=self._var('ignore_allcaps', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Ignore numbers/emails/URLs', variable=self._var('ignore_urls_emails', True)).grid(row=row, column=0, sticky='w')
        row += 1
        ttk.Checkbutton(frm, text='Ignore numbers', variable=self._var('ignore_numbers', True)).grid(row=row, column=0, sticky='w')
        row += 2
        ttk.Button(frm, text='Clear learned pairs', command=self._clear_learned).grid(row=row, column=0, sticky='w')
        row += 2
        btn = ttk.Frame(frm)
        btn.grid(row=row, column=0, sticky='e')
        ttk.Button(btn, text='Cancel', command=self.root.destroy).pack(side='right', padx=4)
        ttk.Button(btn, text='Save', command=self._save).pack(side='right')

    def _clear_learned(self):
        if messagebox.askyesno('TypeFix', 'Clear all learned pairs?'):
            self.cfg.data['learned'] = {}
            self.cfg.save()
            if self.on_changed:
                self.on_changed()

    def _save(self):
        for k, v in self._vars.items():
            self.cfg.data[k] = v.get()
        try:
            from utils.autostart import set_autostart
            set_autostart(bool(self.cfg.data.get('autostart', True)))
        except Exception:
            pass
        self.cfg.save()
        if self.on_changed:
            self.on_changed()
        self.root.destroy()
