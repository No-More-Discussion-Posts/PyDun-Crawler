from setuptools import setup, find_packages

setup(
    name="copd",
    version="0.0.1",
    packages=['copd'],
    entry_points={"console_scripts": ["copd = copd.game:main"]},
    long_description="Simple Dungeon Crawler in Python",
    url="https://github.com/No-More-Discussion-Posts/PyDun-Crawler",
    author="The Team",
)
