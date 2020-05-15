from setuptools import setup
import sys

from taggit_bulk.version import __version__ as version

with open("README.rst", "r") as fp:
    description = fp.read() + "\n"

setup(
    name="django-taggit-bulk",
    version=version,
    description="Bulk update of tags",
    long_description=description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Development Status :: 4 - Beta',
        "Framework :: Django",
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
    keywords="django taggit admin bulk",
    license='LGPL',
    packages=['taggit_bulk'],
    package_data={
        'taggit_bulk': ['templates/taggit_bulk/wizard/form.html']
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django",
        "django-taggit",
        "django-formtools" if sys.version_info.major > 2 else "django-formtools<=2.1",
        "six",
    ],
)
