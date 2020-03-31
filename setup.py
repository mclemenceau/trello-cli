import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "TrelloCli",
    version = "0.0.1",
    author = "Matthieu Clemenceau",
    author_email = "matthieu.clemenceau@canonical.com",
    description = ("A Command Line helper to access Trello Data."),
    license = "GPLv3",
    keywords = "",
    url = "https://github.com/mclemenceau/trello-cli",
    packages=['TrelloCli', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
