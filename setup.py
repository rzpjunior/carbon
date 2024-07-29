from setuptools import setup, find_packages

setup(
    name="carbon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "urwid",
        "kubernetes",
        "PyYAML"
    ],
    entry_points={
        'console_scripts': [
            'carbon=src.main:main',
        ],
    },
)