from setuptools import setup, find_packages

setup(
    name="carbon",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "urwid",
        "kubernetes",
        "PyYAML",
        "ptyprocess",
        "pyte"
    ],
    entry_points={
        'console_scripts': [
            'carbon=src.main:main',
        ],
    },
)