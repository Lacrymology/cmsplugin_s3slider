#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='cmsplugin_s3slider',
    version='0.0.2',
    author='Tomas Neme',
    author_email='lacrymology@gmail.com',
    url='http://github.com/Lacrymology',
    description = 'DjangoCMS image gallery plugin with drag&drop '
                  'reordering in admin, special support for '
                  'thumbnails and s3Slider '
                  'http://www.serie3.info/s3slider/demonstration.html '
                  'Forked from https://github.com/centralniak/cmsplugin_gallery',
    packages=find_packages(),
    provides=['cmsplugin_s3slider', ],
    include_package_data=True,
    install_requires = [
        'django-inline-ordering>=0.1.1',
        'easy-thumbnails',
        'django-sekizai',
        ]
)
