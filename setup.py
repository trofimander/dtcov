# setup.py for Django template coverage.

"""
Django Template Coverage version %(__version__)s
Measures coverage of tags and expression in rendered Django templates.
"""

classifiers = """
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
"""

# Pull in the tools we need.
import sys, traceback


from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup
from distutils.core import Extension    # pylint: disable=E0611,F0401

# Get or massage our metadata.

from dtcov import __url__, __version__

doclines = (__doc__).split('\n')

classifier_list = [c for c in classifiers.split("\n") if c]

if 'a' in __version__:
    devstat = "3 - Alpha"
elif 'b' in __version__:
    devstat = "4 - Beta"
else:
    devstat = "5 - Production/Stable"
classifier_list.append("Development Status :: " + devstat)

setup(
    name = 'django_template_coverage',
    version = __version__,

    packages = [
        'dtcov',
        ],

    package_data = {
    },

    entry_points = {
        'console_scripts': [
            'dtcov = dtcov.run_coverage:main',
            ],
        },

    zip_safe = False,

    author = 'Dmitry Trofimov',
    author_email = 'dmitry.trofimov@jetbrains.com',
    description = doclines[0],
    long_description = '\n'.join(doclines[2:]),
    keywords = 'django code coverage testing',
    license = 'BSD',
    classifiers = classifier_list,
    url = __url__,

    install_requires=[
        "Django >= 1.1",
        "coverage >= 3.5",
        ],
)
