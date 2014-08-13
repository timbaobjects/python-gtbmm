from setuptools import setup

setup(
    name='python-gtbmm',
    version='0.1',
    packages=['gtbmm'],
    author="Tim Akinbo",
    author_email="takinbo@timbaobjects.com",
    url='http://pypi.python.org/pypi/python-gtbmm/',
    license='LICENSE',
    description='A Guaranty Trust Bank Mobile Money interface library',
    long_description=open('README.rst').read(),
    install_requires=[
        "lxml>=3.3.5",
        "pytest>=2.6.0",
        "requests>=2.3.0"
    ],
)
