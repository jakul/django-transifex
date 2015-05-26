from setuptools import setup, find_packages
import sys
import os

from djangotransifex import VERSION


if sys.argv[-1] == 'publish-to-pypi':
    os.system("python setup.py sdist upload -r pypi")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()


if sys.argv[-1] == 'publish-to-pypitest':
    os.system("python setup.py sdist upload -r pypitest")
    sys.exit()


if sys.argv[-1] == 'install-from-pypitest':
    os.system("pip install -i https://testpypi.python.org/pypi djangotransifex")
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
    zip_safe=False,
    include_package_data=True,
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
