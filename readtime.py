from pelican import signals


# We make AVERAGE_READING_WPM a float here so we don't have to make a float()
# call later in the code base.  We do this because we need to get the amount of
# time in fractional minutes and then convert that to total seconds.
AVERAGE_READING_WPM = 275.0
SECONDS_IN_MINUTE = 60


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
        content_support = ["Article"]
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


def register():
    signals.content_object_init.connect(read_time)
