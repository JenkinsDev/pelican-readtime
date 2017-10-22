Readtime plugin for pelican
===================================

Plugin for `Pelican`_ that computes read time based on `Medium's readtime`_
"algorithm".

It adds a ``readtime`` and ``readtime_string`` attributes to every Articles and/or Pages, 
with the time estimation for reading the article.

## Setting Up

#### Adding 'ReadTime' to the list of plugins:
```python
PLUGINS = [ 
	... , 
	'readtime'
]
```

#### 1. Words Per Minute Only

In your settings you would use assign the `READTIME_LANGUAGE_SUPPORT` variable to an integer like so:

***pelicanconf.py***
```
READTIME_LANGUAGE_SUPPORT = 180
```

Every article's read time would  be calculated using this average words per minute count. (See the Usage section for how to use the calculated read times in templates). This is the simplest read time method.

#### 2. Words Per Minute per language

This is the preferred method if you are dealing with multiple languages. Take a look at the following settings


***pelicanconf.py***
```
READTIME_LANGUAGE_SUPPORT = {
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
```

In this example the default reading time for all articles is 200 words per minute. Any articles in spanish will be calculated at 220 wpm. This is useful for information dense languages where the read time varies rapidly.

Chances are the average reading time will not vary rapidly from language to language, however using this method also allows you to set plurals which make templating easier in the long run.

## Usage

Two variables are accessible through the read time plugin, **read_time** and **read_time_string**

```
{% if article.readtime %} This article takes {{article.readtime}} minute(s) to read.{% endif %}
// This article takes 4 minute(s) to read
```

```
{% if article.readtime_string %} This article takes {{article.readtime_string}} to read.{% endif %}
// This article takes 4 minutes to read
```
