import os
import codecs

try:
    from setuptools import (
        setup,
        find_packages
    )

except ImportError:
    from distutils.core import (
        setup,
        find_packages
    )

#######################################################################################################################
#######################################################################################################################

VERSION            = (0, 1, 4)
__version__        = '.'.join(map(str, VERSION[:3])) + "".join(VERSION[3:])

__package_name__   = 'pelican-readtime'
__description__    = 'Plugin for Pelican that computes read time based on Medium\'s readtime "algorithm."'

__contact_names__  = 'David Jenkins, Deepak Bhalla, Jonathan Dektiar'
__contact_emails__ = 'david.nicholas.jenkins@gmail.com; contact@deepakrb.com; contact@jonathandekhtiar.eu;'

__homepage__       = 'https://github.com/JenkinsDev/pelican-readtime'
__repository_url__ = 'https://github.com/JenkinsDev/pelican-readtime'
__download_url__   = 'https://github.com/JenkinsDev/pelican-readtime'

__docformat__      = 'markdown'
__license__        = 'MIT'
__keywords__       = 'pelican blogging blog static webdevelopment plugin pelican-plugin readtime python python3 python2'

#######################################################################################################################
#######################################################################################################################

# Loading the readme file

here = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('README.rst'):
    # codec is used for consistent encoding
    long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf-8').read()
else:
    long_description = 'See ' + __homepage__

# Loading the requirement files

def req_file(filename):
    print("Filename:", filename)
    with codecs.open(os.path.join(here, filename), 'r', 'utf-8') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters
    # Example: `\n` at the end of each line
    return [x.strip() for x in content]

#######################################################################################################################
#######################################################################################################################

# Defining the Package's Setup

setup(
    name = __package_name__,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = __version__,

    description = __description__,
    long_description = long_description,

    # The project's main homepage.
    url = __repository_url__,
    download_url = __download_url__,

    # The licence under which the project is released
    license = 'MIT',

    # Author details
    author = __contact_names__,
    author_email = __contact_emails__,

    # maintainer Details
    maintainer = __contact_names__,
    maintainer_email = __contact_emails__,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    keywords = __keywords__,
    packages = find_packages(exclude=[]),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = req_file("requirements.txt"),

    zip_safe = True,
    include_package_data = True,
)
