import json
import os


class Config:
    def __init__(self):
        self.base = os.path.join(os.environ.get('USERPROFILE', os.path.expanduser('~')), '.typefix')
        os.makedirs(self.base, exist_ok=True)
        self.cfg_path = os.path.join(self.base, 'config.json')
        self.learn_path = os.path.join(self.base, 'learned.json')
        self.data = self._defaults()

    def _defaults(self):
        return {
            'enabled': True,
            'autostart': True,
            'underline_wrong': True,
            'correct_on_space': True,
            'silent': True,
            'show_fix_button': False,
            'ignore_allcaps': True,
            'ignore_urls_emails': True,
            'ignore_numbers': True,
            'lang': 'en',
            'custom_map': {},
            'learned': {},
            'ignore_list': [],
        }

    def load(self):
        try:
            if os.path.exists(self.cfg_path):
                with open(self.cfg_path, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    if isinstance(d, dict):
                        self.data.update(d)
        except Exception:
            pass
        try:
            if os.path.exists(self.learn_path):
                with open(self.learn_path, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    if isinstance(d, dict):
                        self.data['learned'] = d
        except Exception:
            pass

    def save(self):
        try:
            d = dict(self.data)
            learned = d.pop('learned', {}) or {}
            with open(self.cfg_path, 'w', encoding='utf-8') as f:
                json.dump(d, f, indent=2)
            with open(self.learn_path, 'w', encoding='utf-8') as f:
                json.dump(learned, f, indent=2)
        except Exception:
            pass
