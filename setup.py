"""Setup information for the Skytap API package."""
from setuptools import find_packages
from setuptools import setup

setup(
    name='skytap',
    packages=find_packages(),
    version='1.2.0',
    description='Skytap REST API access modules',
    author='Fulcrum Technologies',
    test_suite='nose.collector',
    author_email='bwellington@fulcrum.net',
    maintainer='Michael Knowles',
    maintainer_email='mknowles@fulcrum.net',
    license='MIT',
    install_requires=['requests', 'six'],
    url='https://github.com/FulcrumIT/skytap',
    download_url='https://github.com/FulcrumIT/skytap/tarball/v1.2.0',
    keywords=['skytap', 'cloud', 'client', 'rest', 'api', 'development'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Internet"
    ]
)
