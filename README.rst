Readtime plugin for pelican
===========================

.. image:: https://travis-ci.com/JenkinsDev/pelican-readtime.svg?branch=master
    :target: https://travis-ci.com/JenkinsDev/pelican-readtime

Plugin for `Pelican`_ that computes a piece of content's read time.

It adds a ``readtime`` and ``readtime_string`` attributes to every
article and/or page, with the time estimation for reading the article.

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
            'min_plural': 'minutes',
            'sec_singular': 'second',
            'sec_plural': 'seconds'
        },
        'es': {
            'wpm': 220,
            'min_singular': 'minuto',
            'min_plural': 'minutos',
            'sec_singular': 'segundo',
            'sec_plural': 'segundos'
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

Four variables are accessible through the read time plugin:
**readtime**, **readtime\_string**, **readtime\_with\_seconds**, and **readtime\_string\_with\_seconds**

.. code:: html

    {% if article.readtime %} This article takes {{article.readtime}} minute(s) to read.{% endif %}
    // This article takes 4 minute(s) to read.

.. code:: html

    {% if article.readtime_string %} This article takes {{article.readtime_string}} to read.{% endif %}
    // This article takes 4 minutes to read.

.. code:: html

    {% if article.readtime_with_seconds %}
      This article takes {{article.read_with_seconds[0]}} minutes(s) and {{article.read_with_seconds[1]}} second(s) to read.
    {% endif %}
    // This article takes 4 minutes and 21 second(s) to read.

.. code:: html

    {% if article.readtime_string_with_seconds %} This article takes {{article.readtime_string_with_seconds}} to read.{% endif %}
    // This article takes 4 minutes, 1 second to read.


Links
-----

.. _Pelican: http://getpelican.com/
