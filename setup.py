from setuptools import setup, find_packages
import sys
import os

from djangotransifex import VERSION


if sys.argv[-1] == 'publish-to-pypi':
    os.system("python setup.py sdist upload -r pypi")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()


setup(
    name='djangotransifex',
    version=VERSION,
    description='A Django api to Transifex',
    author='Craig Blaszczyk',
    author_email='masterjakul@gmail.com',
    url='https://github.com/jakul/django-transifex',
    license='BSD',
    packages=find_packages(),
    tests_require=[
    ],
    install_requires=open('requirements.txt').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
