from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator


# We make AVERAGE_READING_WPM a float here so we don't have to make a float()
# call later in the code base.  We do this because we need to get the amount of
# time in fractional minutes and then convert that to total seconds.
AVERAGE_READING_WPM = 275.0
SECONDS_IN_MINUTE = 60

class ReadTimeParser(object):
    def __init__(self):
        self.data = {
            'default': {
                'wpm': 200,
                'plurals': [
                    'minute',
                    'minutes'
                ]
            }
        }

        settings_wpm = generator.settings.get('READ_TIME', data)

        # Allows a wpm entry
        if isinstance(settings_wpm, int):
            self.data['default']['wpm'] = settings_wpm

        # Default checker
        elif isinstance(settings_wpm, dict):
            if 'default' not in settings_wpm:
                pass
            elif 'wpm' not in settings_wpm['default']:
                pass
            elif 'plurals' not in settings_wpm['default']:
                pass
            elif not isinstance(settings_wpm['default']['wpm'], int):
                pass
            elif not isinstance(settings_wpm['default']['plurals'], list):
                pass
            elif len(settings_wpm['default']['plurals']) != 2:
                pass
            else:
                data = settings_wpm

readtime_parser = ReadTimeParser()

def read_time(content):
    """ Core function used to generate the read_time for content. Readtime is
    algorithmically computed based on Medium's readtime functionality.
    Read: https://medium.com/the-story/read-time-and-you-bc2048ab620c

    Parameters:
        :param content: Sub-Instance of pelican.content.Content

    Returns:
        None
    """

    if content_type_supported(content):
        # We get the content's text, split it at the spaces and check the
        # length of the provided array to get a good estimation on the amount
        # of words in the content.
        words = len(content._content.split())
        #words = len(content.content.split())
        read_time_seconds = round((words / AVERAGE_READING_WPM) * 60, 2)
        minutes, seconds = get_time_from_seconds(read_time_seconds)
        minutes_str = pluralize(minutes, "Minute", "Minutes")
        seconds_str = pluralize(seconds, "Second", "Seconds")
        content.readtime = "{} and {}".format(minutes_str, seconds_str)
        content.readtime_minutes = minutes + int(bool(seconds))



def pluralize(measure, singular, plural):
    """ Returns a string that contains the measure (amount) and its plural or
    singular form depending on the amount.

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


def get_time_from_seconds(read_time_seconds):
    """ Returns, in a tuple, the amount of minutes and seconds based on the
    provided seconds.  87 seconds would return (1, 27); 1 minute and 27 seconds.

    Parameters:
        :param read_time_seconds: The amount of seconds to retrieve time from.

    Returns:
        Tuple containing minutes and seconds
    """
    minutes = int(read_time_seconds / SECONDS_IN_MINUTE)
    seconds = int(read_time_seconds % SECONDS_IN_MINUTE)
    return minutes, seconds


def content_type_supported(content):
    """ Returns an answer to whether the content instance supplied is supported
    by the current configuration.

    Parameters:
        :param content: Sub-Instance of pelican.content.Content

    Returns:
        None
    """
    if "READTIME_CONTENT_SUPPORT" in content.settings:
        content_support = content.settings["READTIME_CONTENT_SUPPORT"]
    else:
        content_support = ["Article, Page"]
    return class_name(content) in content_support


def class_name(obj):
    """ A form of python reflection, returns the human readable, string formatted,
    version of a class's name.

    Parameters:
        :param obj: Any object.

    Returns:
        A human readable string version of the supplied object's class name.
    """
    return obj.__class__.__name__


def run_read_time(generators):

    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                read_time(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                read_time(page)


def register():
    try:
        signals.all_generators_finalized.connect(run_read_time)
    except AttributeError:
        # This leads to problem parsing internal links with '{filename}'
        signals.content_object_init.connect(read_time)
