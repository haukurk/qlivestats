from setuptools import setup, find_packages

setup(
    name="qlivestats",
    version="0.1.1",
    description="Tool to simplify querying Livestats broker for Nagios",
    author="@haukurk",
    author_email="haukur@hauxi.is",
    packages=['qlivestats','qlivestats.core'],
    package_data = {
        '': ['*.yaml']
    },
    include_package_data = True,
    install_requires=['Click'],
    url='https://github.com/haukurk/qlivestats',
    download_url='https://github.com/haukurk/qlivestats/releases/tag/v0.1.0',
    keywords=['nagios', 'livestats'],
    test_requires=['mock'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'qlivestats=qlivestats:qlivestatsquery',
            'qlivestats-describe=qlivestats:qlivestatsdescribe'
        ],
    }
)
