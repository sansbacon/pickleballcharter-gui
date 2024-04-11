from setuptools import setup, find_packages

setup(
    name='pbcgui',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pbc = app:main',
        ],
    },
)