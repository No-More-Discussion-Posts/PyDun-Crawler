from setuptools import setup,find_packages

setup(
    name='pydun-crawler',
    version='0.0.1',
    packages=find_packages("src"),
    package_dir={"":"src"},
    entry_points = {
        'console_scripts': [
            'pydun = game:main',
        ]
    },
    long_description='Simple Dungeon Crawler in Python',
    url='https://github.com/No-More-Discussion-Posts/PyDun-Crawler',
    author='The Team'
)