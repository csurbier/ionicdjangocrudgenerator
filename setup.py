import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ionicdjangocrudgenerator',
    version='1.0.0',

    description='Create Django Rest Framework API (Views,Serializers,urls) and Ionic API services (C.R.U.D).',
    long_description=README,

    url='https://github.com/csurbier/ionicdjangocrudgenerator',
    download_url = 'https://github.com/csurbier/ionicdjangocrudgenerator/archive/1.0.0.zip',
    author='Christophe Surbier',
    author_email='csurbier@idevotion.fr',

    license='MIT',

    packages=['ionicdjangocrudgenerator', 'ionicdjangocrudgenerator.templates','ionicdjangocrudgenerator.templates.django','ionicdjangocrudgenerator.templates.ionic','ionicdjangocrudgenerator.templatetags', 'ionicdjangocrudgenerator.management', 'ionicdjangocrudgenerator.management.commands'],
    include_package_data=True,
    install_requires=['Django>=1.11'],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],

    keywords='Django API REST framework generate scaffold and Ionic APIServices scaffold',
)
