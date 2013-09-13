import unittest

class test_imports(unittest.TestCase):

    def test_django(self):
        import django

    def test_symposion(self):
        import symposion

    def test_pinax_theme_bootstrap(self):
        import pinax_theme_bootstrap

    def test_django_forms_bootstrap(self):
        import django_forms_bootstrap

    def test_metron(self):
        import metron

    def test_pinax_utils(self):
        import pinax_utils

    def test_django_debug_toolbar(self):
        import debug_toolbar

    def test_django_mailer(self):
        import mailer

    def test_django_timezones(self):
        import timezones

    def test_pytz(self):
        import pytz

    def test_django_model_utils(self):
        import model_utils

    def test_django_taggit(self):
        import taggit

    def test_django_reversion(self):
        import reversion

    def test_django_markitup(self):
        import markitup

    def test_markdown(self):
        import markdown

    def test_django_sitetree(self):
        import sitetree

    def test_PIL(self):
        import PIL

    def test_easy_thumbnails(self):
        import easy_thumbnails

    def test_eventbrite(self):
        import eventbrite


class test_dbStuff(unittest.TestCase):
    '''test for stuff requiring django settings'''

    def test_Reversion(self):
        from django.conf import settings
        settings.configure(DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'my_db'
            }})
        import reversion


if __name__ == "__main__":
    unittest.main()
