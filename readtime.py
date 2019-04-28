from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator


class ReadTimeParser(object):

    def __init__(self):
        self.initialized = False
        self.content_type_supported = ["Article", "Page", "Draft"]
        self.language_settings = {
            'default': {
                'wpm': 200,
                'min_singular': 'minute',
                'min_plural': 'minutes'
            }
        }

    def set_settings(self, sender):
        try:
            self.initialized = True
            settings_contenttype = sender.settings.get(
                'READTIME_CONTENT_SUPPORT', self.content_type_supported)

            if not isinstance(settings_contenttype, list):
                raise Exception(
                    "Settings 'READTIME_CONTENT_SUPPORT' must be a list")
            else:
                self.content_type_supported = settings_contenttype

            settings_wpm = sender.settings.get(
                'READTIME_WPM', self.language_settings)

            # Allows a wpm entry
            if isinstance(settings_wpm, int):
                self.language_settings['default']['wpm'] = settings_wpm

            # Default checker
            elif isinstance(settings_wpm, dict):
                if 'default' not in settings_wpm:
                    pass
                else:

                    for key in settings_wpm.keys():

                        if "wpm" not in settings_wpm[key]:
                            raise Exception("Missing wpm value for the language: {}".format(key))

                        if not isinstance(settings_wpm[key]['wpm'], int):
                            raise Exception("WPM is not an integer for the language: {}".format(key))

                        if "min_singular" not in settings_wpm[key]:
                            raise Exception("Missing singular form for the language: {}".format(key))

                        if "min_plural" not in settings_wpm[key]:
                            raise Exception("Missing plural form for the language: {}".format(key))

                    self.language_settings = settings_wpm

        except Exception as e:
            raise Exception("ReadTime Plugin: %s" % str(e))

    def read_time(self, content):
        """ Core function used to generate the read_time for content. Readtime is
        algorithmically computed based on Medium's readtime functionality.
        Read: https://medium.com/the-story/read-time-and-you-bc2048ab620c

        Parameters:
            :param content: Sub-Instance of pelican.content.Content

        Returns:
            None
        """

        if self.class_name(content) in self.content_type_supported:
            language = 'default'
            if content.lang in self.language_settings:
                language = content.lang

            # Exit if read time is set by article
            if hasattr(content, 'readtime'):
                return None

            avg_reading_wpm = self.language_settings[language]["wpm"]
            num_words = len(content._content.split())

            read_time_seconds = round((num_words / avg_reading_wpm) * 60, 2)
            read_time_minutes = int(read_time_seconds / avg_reading_wpm)

            minutes_str = self.pluralize(
                read_time_minutes,
                self.language_settings[language]["min_singular"], # minute
                self.language_settings[language]["min_plural"]    # minutes
            )

            content.readtime = "{}".format(read_time_minutes)
            content.readtime_string = "{}".format(minutes_str)

    def pluralize(self, measure, singular, plural):
        """ Returns a string that contains the measure (amount) and its plural
        or singular form depending on the amount.

        Parameters:
            :param measure: Amount, value, always a numerical value
            :param singular: The singular form of the chosen word
            :param plural: The plural form of the chosen word

        Returns:
            String
        """
        if measure == 1:
            return "{} {}".format(measure, singular)
        else:
            return "{} {}".format(measure, plural)

    def class_name(self, obj):
        """ A form of python reflection, returns the human readable, string
        formatted, version of a class's name.

        Parameters:
            :param obj: Any object.

        Returns:
            A human readable str of the supplied object's class name.
        """
        return obj.__class__.__name__


READTIME_PARSER = ReadTimeParser()


def run_read_time(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                READTIME_PARSER.read_time(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                READTIME_PARSER.read_time(page)


def initialize_parser(sender):
    if not READTIME_PARSER.initialized:
        READTIME_PARSER.set_settings(sender)


def register():
    signals.initialized.connect(initialize_parser)

    try:
        signals.all_generators_finalized.connect(run_read_time)
    except Exception as e:
        raise ("ReadTime Plugin: Error during 'register' process: {}".format(str(e)))
