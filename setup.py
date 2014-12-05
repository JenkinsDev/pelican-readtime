import os

from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='pelican-readtime',
    version='0.1.1',
    description='Plugin for Pelican that computes read time based on Medium\'s readtime "algorithm."',
    long_description='Plugin for Pelican that computes read time based on Medium\'s readtime "algorithm."',
    url='https://github.com/JenkinsDev/pelican-readtime',
    license='MIT',
    author='David Jenkins',
    author_email='david.nicholas.jenkins@gmail.com',
    py_modules=['readtime'],
    requires=['pelican'],
    include_package_data=True,
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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
