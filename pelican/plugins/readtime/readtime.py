from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator


class ReadTimeParser(object):

    def __init__(self):
        self.initialized = False
        self.content_type_supported = ["Article", "Page", "Draft"]
        self.lang_settings = {
            'default': {
                'wpm': 200,
                'min_singular': 'minute',
                'min_plural': 'minutes',
                'sec_singular': 'second',
                'sec_plural': 'seconds'
            }
        }

    def _set_supported_content_type(self, content_types_supported):
        """ Checks and sets the supported content types configuration value.
        """
        if not isinstance(content_types_supported, list):
            raise TypeError(("Settings 'READTIME_CONTENT_SUPPORT' must be"
                             "a list of content types."))

        self.content_type_supported = content_types_supported

    def _set_lang_settings(self, lang_settings):
        """ Checks and sets the per language WPM, singular and plural values.
        """
        is_int = isinstance(lang_settings, int)
        is_dict = isinstance(lang_settings, dict)
        if not is_int and not is_dict:
            raise TypeError(("Settings 'READTIME_WPM' must be either an int,"
                             "or a dict with settings per language."))

        # For backwards compatability reasons we'll allow the
        # READTIME_WPM setting to be set as an to override just the default
        # set WPM.
        if is_int:
            self.lang_settings['default']['wpm'] = lang_settings
        elif is_dict:
            for lang, conf in lang_settings.items():
                if 'wpm' not in conf:
                    raise KeyError(('Missing wpm value for the'
                                    'language: {}'.format(lang)))

                if not isinstance(conf['wpm'], int):
                    raise TypeError(('WPM is not an integer for'
                                     ' the language: {}'.format(lang)))

                if "min_singular" not in conf:
                    raise KeyError(('Missing singular form for "minute" for'
                                    ' the language: {}'.format(lang)))

                if "min_plural" not in conf:
                    raise KeyError(('Missing plural form for "minutes" for'
                                    ' the language: {}'.format(lang)))

                if "sec_singular" not in conf:
                    raise KeyError(('Missing singular form for "second" for'
                                    ' the language: {}'.format(lang)))

                if "sec_plural" not in conf:
                    raise KeyError(('Missing plural form for "seconds" for'
                                    ' the language: {}'.format(lang)))

            self.lang_settings = lang_settings

    def initialize_settings(self, sender):
        """ Initializes ReadTimeParser with configuration values set by the
        site author.
        """
        try:
            self.initialized = True

            settings_content_types = sender.settings.get(
                'READTIME_CONTENT_SUPPORT', self.content_type_supported)
            self._set_supported_content_type(settings_content_types)

            lang_settings = sender.settings.get(
                'READTIME_WPM', self.lang_settings)
            self._set_lang_settings(lang_settings)
        except Exception as e:
            raise Exception("ReadTime Plugin: %s" % str(e))

    def read_time(self, content):
        """ Core function used to generate the read_time for content.

        Parameters:
            :param content: Instance of pelican.content.Content

        Returns:
            None
        """
        if get_class_name(content) in self.content_type_supported:
            # Exit if readtime is already set
            if hasattr(content, 'readtime'):
                return None

            default_lang_conf = self.lang_settings['default']
            lang_conf = self.lang_settings.get(content.lang, default_lang_conf)
            avg_reading_wpm = lang_conf['wpm']

            num_words = len(content._content.split())
            # Floor division so we don't have to convert float -> int
            minutes = num_words // avg_reading_wpm
            # Get seconds to read, then subtract our minutes as seconds from
            # the time to get remainder seconds
            seconds = int((num_words / avg_reading_wpm * 60) - (minutes * 60))

            minutes_str = self.pluralize(
                minutes,
                lang_conf['min_singular'],
                lang_conf['min_plural']
            )

            seconds_str = self.pluralize(
                seconds,
                lang_conf['sec_singular'],
                lang_conf['sec_plural']
            )

            content.readtime = minutes
            content.readtime_string = minutes_str
            content.readtime_with_seconds = (minutes, seconds,)
            content.readtime_string_with_seconds = "{}, {}".format(
                minutes_str, seconds_str)

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


READTIME_PARSER = ReadTimeParser()


def get_class_name(obj):
    """ A form of python reflection, returns the human readable, string
    formatted, version of a class's name.

    Parameters:
        :param obj: Any object.

    Returns:
        A human readable str of the supplied object's class name.
    """
    return obj.__class__.__name__


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
        READTIME_PARSER.initialize_settings(sender)


def register():
    signals.initialized.connect(initialize_parser)

    try:
        signals.all_generators_finalized.connect(run_read_time)
    except Exception as e:
        raise "ReadTime Plugin: Error during 'register' process: {}".format(str(e))
