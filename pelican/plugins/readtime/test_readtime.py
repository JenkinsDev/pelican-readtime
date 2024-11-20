import unittest
import random

from readtime import ReadTimeParser


TEST_WPM = 123


class TestReadTime(unittest.TestCase):

    def setUp(self):
        self.READTIME_CONTENT_SUPPORT = ["Article", "Page", "Draft"]
        self.READTIME_WPM = {
            'default': {
                'wpm': TEST_WPM,
                'min_singular': 'minute',
                'min_plural': 'minutes',
                'sec_singular': 'second',
                'sec_plural': 'seconds'
            },
            'devil': {
                'wpm': 666,
                'min_singular': 'inferno',
                'min_plural': 'infernos',
                'sec_singular': 'hellhound',
                'sec_plural': 'hellhounds'
            }
        }

        self.sender = Sender(self.READTIME_CONTENT_SUPPORT, self.READTIME_WPM)

        self.READTIME_PARSER = ReadTimeParser()
        self.READTIME_PARSER.initialize_settings(self.sender)

    def assert_document_has_readtime_attributes(self, document):
        class_name = document.__class__.__name__
        self.assertTrue(
            hasattr(document, 'readtime'),
            "readtime property is not defined for an {}".format(class_name)
        )
        self.assertTrue(
            hasattr(document, 'readtime_string'),
            "readtime_string property is not defined for an {}".format(
                class_name)
        )
        self.assertTrue(
            hasattr(document, 'readtime_with_seconds'),
            "readtime_with_seconds property is not defined for an {}".format(
                class_name)
        )
        self.assertTrue(
            hasattr(document, 'readtime_string_with_seconds'),
            "readtime_string_with_seconds property is not defined for an {}".format(
                class_name)
        )

    def test_parse_article(self):
        article = Article(754)
        self.READTIME_PARSER.read_time(article)
        self.assert_document_has_readtime_attributes(article)

        self.assertEqual(article.readtime, 6)
        self.assertEqual(article.readtime_with_seconds, (6, 7))
        self.assertEqual(article.readtime_string, "6 minutes")
        self.assertEqual(
            article.readtime_string_with_seconds, "6 minutes, 7 seconds")

    def test_parse_page(self):
        page = Page(123)
        self.READTIME_PARSER.read_time(page)
        self.assert_document_has_readtime_attributes(page)

        self.assertEqual(page.readtime, 1)
        self.assertEqual(page.readtime_with_seconds, (1, 0))
        self.assertEqual(page.readtime_string, "1 minute")
        self.assertEqual(
            page.readtime_string_with_seconds, "1 minute, 0 seconds")

    def test_parse_draft(self):
        draft = Draft(865)
        self.READTIME_PARSER.read_time(draft)
        self.assert_document_has_readtime_attributes(draft)

        self.assertEqual(draft.readtime, 7)
        self.assertEqual(draft.readtime_with_seconds, (7, 1))
        self.assertEqual(draft.readtime_string, "7 minutes")
        self.assertEqual(
            draft.readtime_string_with_seconds, "7 minutes, 1 second")

    def test_parse_not_article(self):
        article = UnsupportedArticle(754)
        self.READTIME_PARSER.read_time(article)

        self.assertFalse(
            hasattr(article, 'readtime'),
            "readtime property is not defined for an UnsupportedArticle"
        )
        self.assertFalse(
            hasattr(article, 'readtime_string'),
            "readtime_string property is not defined for an UnsupportedArticle"
        )
        self.assertFalse(
            hasattr(article, 'readtime_with_seconds'),
            "readtime_with_seconds property is not defined for an UnsupportedArticle"
        )
        self.assertFalse(
            hasattr(article, 'readtime_string_with_seconds'),
            "readtime_string_with_seconds property is not defined for an UnsupportedArticle"
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
