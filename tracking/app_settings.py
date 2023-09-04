

class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    
    def _settings(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)
    

    @property
    def PATH_LENGTH(self):
        return self._settings('PATH_LENGTH', 200)


app_settings = AppSettings('DRF_TRACKING')
