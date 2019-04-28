import os
import codecs

try:
    from setuptools import (setup, find_packages)
except ImportError:
    from distutils.core import (setup, find_packages)


VERSION = (0, 1, 7)
__version__ = '.'.join(map(str, VERSION[:3])) + "".join(VERSION[3:])

__package_name__ = 'pelican-readtime'
__description__ = 'Plugin for Pelican that computes average read time.'

__contact_names__ = 'David Jenkins, Deepak Bhalla, Jonathan Dektiar'
__contact_emails__ = 'djenkinsdev@gmail.com, contact@deepakrb.com, contact@jonathandekhtiar.eu'

__homepage__ = 'https://github.com/JenkinsDev/pelican-readtime'
__repository_url__ = 'https://github.com/JenkinsDev/pelican-readtime'
__download_url__ = 'https://github.com/JenkinsDev/pelican-readtime'

__docformat__ = 'markdown'
__license__ = 'MIT'
__keywords__ = 'pelican blogging blog static webdevelopment plugin pelican-plugin readtime python python3 python2'


here = os.path.abspath(os.path.dirname(__file__))
if os.path.exists('README.rst'):
    # codec is used for consistent encoding
    long_description = codecs.open(
        os.path.join(here, 'README.rst'), 'r', 'utf-8').read()
else:
    long_description = 'See ' + __homepage__

setup(
    name=__package_name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    url=__repository_url__,
    download_url=__download_url__,
    license='MIT',
    author=__contact_names__,
    author_email=__contact_emails__,
    maintainer=__contact_names__,
    maintainer_email=__contact_emails__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=__keywords__,
    packages=[''],
    install_requires=['pelican>=3.6'],
    zip_safe=True,
    include_package_data=True
)
