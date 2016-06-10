Readtime plugin for pelican
===========================

Plugin for `Pelican`_ that computes read time based on `Medium's readtime`_
"algorithm".
It adds a ``readtime`` and ``readtime_minutes`` attributes to articles, with
the time estimation for reading the article.

Usage
-----

To use it you have to add the plugin name to the ``pelicanconf.py`` file.

.. code:: python

	PLUGINS=[ ... , 'readtime']

Then you can access the ``readtime`` variable to show read time estimation on
your templates.

.. code:: html

  {% if article.readtime %} <div>{{ article.readtime }} read</div> {% endif %}

It will generate the following:

.. code:: html

  <div>X Minutes and Y Seconds read</div>

Alternatively, you can use the ``readtime_minutes`` variable to get the number
of minutes instead of the fully formatted text.

.. _`Pelican`: http://getpelican.com/
.. _`Medium's readtime`: https://help.medium.com/hc/en-us/articles/214991667-Read-time
