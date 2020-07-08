from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='depq',
    version='0.1',
    description='Double-ended priority queue',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='KiranBaktha (modified by Cameron Allen)',
    author_email=('csal@brown.edu'),
    packages=find_packages(include=['depq', 'depq.*']),
    url='https://github.com/camall3n/depq/',
)
