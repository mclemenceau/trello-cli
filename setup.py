import setuptools

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="TrelloCli",
    version="0.0.4",
    author="Matthieu Clemenceau",
    author_email="matthieu.clemenceau@canonical.com",
    description=("A Command Line helper to access Trello Data."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mclemenceau/trello-cli",
    project_urls={
        'Bug Reports': 'https://github.com/mclemenceau/trello-cli/issues',
        'Source': 'https://github.com/mclemenceau/trello-cli/',
    },
    packages=setuptools.find_packages(),
    keywords='trello cli',
    entry_points={
        'console_scripts': [
            'trello-cli=TrelloCli.main:main',
        ],
    },
    install_requires=['py-trello'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
