import setuptools
from setuptools import setup, find_packages
from piVibe import about

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name=about.package,
    version=about.version,
    author=about.author,
    author_email=about.author_email,
    description=about.description,
    long_description=long_description,
    url=about.url,
    packages=find_packages(exclude=['htmlcov', 'testing', '.vscode', 'docs']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'Click',
        'colorzero',
        'dominate',
        'Flask',
        'Flask-Bootstrap',
        'gpiozero',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'python-dotenv',
        'PyYAML',
        'visitor',
        'Werkzeug'
        ]
)
