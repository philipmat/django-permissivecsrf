import os
from setuptools import setup


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rt')
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    # Basic package information
    name='django-permissivecsrf',
    version='1.0.0',
    packages=('permissivecsrf',),

    # test_suite='tests.runtests.main',

    # Packaging options
    include_package_data=True,
    install_requires = ['Django>=1.0'],

    # Metadata for PyPI
    url="https://github.com/philipmat/django-permissivecsrf",
    description='More permissive CSRF check for Django when moving between HTTP and HTTPS',
    long_description=long_description,
    author='Philip Mateescu',
    author_email='dev@philipm.at',
    license='BSD',
    keywords='django CSRF'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)

