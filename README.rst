Readtime plugin for pelican
===========================

Plugin for `Pelican`_ that computes read time based on `Medium’s readtime`_ “algorithm”.

It adds a ``readtime`` and ``readtime_string`` attributes to every
Articles and/or Pages, with the time estimation for reading the article.

Setting Up
----------

Adding ‘ReadTime’ to the list of plugins:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**In pelicanconf.py:**

.. code:: python

    PLUGINS = [
        ... ,
        'readtime'
    ]

1. Words Per Minute Only
^^^^^^^^^^^^^^^^^^^^^^^^

In your settings you would use assign the ``READTIME_WPM`` variable to
an integer like so:

**In pelicanconf.py:**

.. code:: python

    READTIME_WPM = 180

Every article’s read time would be calculated using this average words
per minute count. (See the Usage section for how to use the calculated
read times in templates). This is the simplest read time method.

2. Words Per Minute per language
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the preferred method if you are dealing with multiple languages.
Take a look at the following settings

**In pelicanconf.py:**

.. code:: python

    READTIME_WPM = {
        'default': {
            'wpm': 200,
            'min_singular': 'minute',
            'min_plural': 'minutes'
        },
        'es': {
            'wpm': 220,
            'min_singular': 'minuto',
            'min_plural': 'minutos'
        }
    }

In this example the default reading time for all articles is 200 words
per minute. Any articles in spanish will be calculated at 220 wpm. This
is useful for information dense languages where the read time varies
rapidly.

Chances are the average reading time will not vary rapidly from language
to language, however using this method also allows you to set plurals
which make templating easier in the long run.

Usage
-----

Two variables are accessible through the read time plugin,
**read\_time** and **read\_time\_string**

.. code:: html

    {% if article.readtime %} This article takes {{article.readtime}} minute(s) to read.{% endif %}
    // This article takes 4 minute(s) to read

.. code:: html

    {% if article.readtime_string %} This article takes {{article.readtime_string}} to read.{% endif %}
    // This article takes 4 minutes to read

Disclaimer
----------

This repository is reworked plugin which integrates some of the best of
two existing plugins:

-  https://github.com/deepakrb/Pelican-Read-Time
-  https://github.com/JenkinsDev/pelican-readtime

The objective was to fix a few issues and to improve (from my point of
view) the overall behavior.

.. _Pelican: http://getpelican.com/
.. _Medium’s readtime: https://help.medium.com/hc/en-us/articles/214991667-Read-time
