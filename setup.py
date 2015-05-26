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
    install_requires=['Click==4.0.0','pyyaml','simplejson'],
    url='https://github.com/haukurk/qlivestats',
    download_url='https://github.com/haukurk/qlivestats/releases/tag/v0.1.1',
    keywords=['nagios', 'livestats'],
    tests_require=['pytest', 'tox', 'mock', 'coverage', 'coveralls'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'qlivestats=qlivestats:qlivestatsquery',
            'qlivestats-describe=qlivestats:qlivestatsdescribe'
        ],
    }
)
