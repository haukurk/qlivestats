from setuptools import setup

setup(
    name="qlivestats",
    version="0.1.0",
    description="Tool to simplify querying Livestats broker for Nagios",
    author="@haukurk",
    author_email="haukur@hauxi.is",
    packages=["qlivestats"],
    install_requires=[],
    url='https://github.com/haukurk/qlivestats',
    download_url='https://github.com/haukurk/qlivestats/releases/tag/v0.1.0',
    keywords=['nagios', 'livestats'],
    test_requires=['tox', 'mock', 'pytest'],
    classifiers=[],
    entry_points={
        'console_scripts': ['qlivestats=qlivestats.__main__:default'],
    }
)
