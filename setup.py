from setuptools import setup,find_packages

setup(
    name='pydun-crawler',
    version='0.0.1',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'pydun = src.game:main',
        ]
    },
    long_description='Simple Dungeon Crawler in Python',
    url='https://github.com/No-More-Discussion-Posts/PyDun-Crawler',
    author='The Team'
)