import finddata
from setuptools import setup, find_packages

setup(
    name="django-hotspots",
    author="Jonas und der Wolf GmbH",
    author_email="info@jonasundderwolf.de",
    version='0.1',
    packages=find_packages(),
    package_data=finddata.find_package_data(),
    include_package_data=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
