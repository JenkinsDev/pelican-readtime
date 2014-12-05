import unittest

from readtime import get_time_from_seconds, content_type_supported, pluralize


class TestReadTime(unittest.TestCase):

    SINGULAR_SECONDS = "Second"
    PLURAL_SECONDS = "Seconds"

    def test_get_time_from_seconds_returns_correct_amount_of_time(self):
        minutes, seconds = get_time_from_seconds(87)
        self.assertEquals(minutes, 1)
        self.assertEquals(seconds, 27)
        minutes, seconds = get_time_from_seconds(120)
        self.assertEquals(minutes, 2)
        self.assertEquals(seconds, 0)

    def test_content_type_supported(self):
        content = Content(content_support=["Content"])
        self.assertTrue(content_type_supported(content))

        content = Content(content_support=["NoArticle", "Page"])
        self.assertFalse(content_type_supported(content))

    def test_pluralize_minutes(self):
        singular = "Minute"
        plural = "Minutes"
        minute = 1
        minutes = 20
        self.assertEquals("1 Minute", pluralize(minute, singular, plural))
        self.assertEquals("20 Minutes", pluralize(minutes, singular, plural))

    def test_pluralize_seconds(self):
        singular = "Second"
        plural = "Seconds"
        second = 1
        seconds = 20
        self.assertEquals("1 Second", pluralize(second, singular, plural))
        self.assertEquals("20 Seconds", pluralize(seconds, singular, plural))


class Content():

    def __init__(self, content_support):
        self.settings = { "READTIME_CONTENT_SUPPORT": content_support }


if __name__ == "__main__":
    unittest.main()
