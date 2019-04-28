import unittest
import random

from readtime import ReadTimeParser


class TestReadTime(unittest.TestCase):

    def setUp(self):
        self.READTIME_CONTENT_SUPPORT = ["Article", "Page", "Draft"]
        self.READTIME_WPM = {
            'default': {
                'wpm': 123,
                'min_singular': 'minute',
                'min_plural': 'minutes'
            },
            'devil': {
                'wpm': 666,
                'min_singular': 'inferno',
                'min_plural': 'infernos'
            }
        }

        self.sender = Sender(self.READTIME_CONTENT_SUPPORT, self.READTIME_WPM)

        self.READTIME_PARSER = ReadTimeParser()
        self.READTIME_PARSER.set_settings(self.sender)

    def test_parse_article(self):
        article = Article(754)

        raised = False
        error = ''
        try:
            self.READTIME_PARSER.read_time(article)

        except Exception as e:
            error = str(e)
            raised = True

        self.assertFalse(raised, error)
        self.assertTrue(
            hasattr(article, 'readtime'),
            "readtime property is not defined for an Article"
        )
        self.assertTrue(
            hasattr(article, 'readtime_string'),
            "readtime_string property is not defined for an Article"
        )

    def test_parse_page(self):
        article = Page(754)

        raised = False
        error = ''
        try:
            self.READTIME_PARSER.read_time(article)

        except Exception as e:
            error = str(e)
            raised = True

        self.assertFalse(raised, error)
        self.assertTrue(
            hasattr(article, 'readtime'),
            "readtime property is not defined for an Article"
        )
        self.assertTrue(
            hasattr(article, 'readtime_string'),
            "readtime_string property is not defined for an Article"
        )


    def test_parse_not_article(self):
        article = UnsupportedArticle(754)

        raised = False
        error = ''
        try:
            self.READTIME_PARSER.read_time(article)

        except Exception as e:
            error = str(e)
            raised = True

        self.assertFalse(raised, error)
        self.assertFalse(
            hasattr(article, 'readtime'),
            "readtime property should not be defined for an UnsupportedArticle"
        )
        self.assertFalse(
            hasattr(article, 'readtime_string'),
            "readtime_string property should not be defined for an UnsupportedArticle"
        )

    def test_parse_draft(self):
        article = Draft(754)

        raised = False
        error = ''
        try:
            self.READTIME_PARSER.read_time(article)

        except Exception as e:
            error = str(e)
            raised = True

        self.assertFalse(raised, error)
        self.assertTrue(
            hasattr(article, 'readtime'),
            "readtime property is not defined for a Draft"
        )
        self.assertTrue(
            hasattr(article, 'readtime_string'),
            "readtime_string property is not defined for a Draft"
        )


class Sender():
    def __init__(self, content_support, wpm):
        self.settings = {
            "READTIME_CONTENT_SUPPORT": content_support,
            "READTIME_WPM": wpm
        }


class BaseArticle(object):
    def __init__(self, word_length=200, **kwargs):
        word_list = [
            'knit', 'perfect', 'low', 'absent', 'waves', 'phobic', 'glove',
            'unable', 'garrulous', 'abhorrent', 'annoyed', 'jittery',
            'pink', 'store', 'wood', 'prevent', 'remove', 'voice',
            'slip', 'puncture', 'wind', 'noise', 'faithful', 'grip',
            'street', 'size', 'macho', 'tested', 'gentle', 'ill-fated',
            'placid', 'vase', 'refuse', 'protest', 'grade',
            'approval', 'adorable', 'collar', 'animal', 'toad'
        ]

        self.lang = 'en'

        self._content = ""
        for _ in range(word_length):
            if _ != 0:
                self._content += " "

            self._content += random.choice(word_list)


class Draft(BaseArticle):
    pass


class Article(BaseArticle):
    pass


class Page(BaseArticle):
    pass


class UnsupportedArticle(BaseArticle):
    pass


if __name__ == "__main__":
    unittest.main()
