from os import path
from setuptools import setup, find_packages

with open(path.join(path.dirname(__file__), 'pytsite', 'VERSION.txt')) as f:
    VERSION = f.readline().replace('\n', '')

setup(
    name='pytsite',
    version=VERSION,
    description='Brand New Python Web Framework',
    url='https://pytsite.xyz',
    download_url='https://github.com/pytsite/pytsite/archive/{}.tar.gz'.format(VERSION),
    author='Alexander Shepetko',
    author_email='a@shepetko.com',
    license='MIT',
    install_requires=[
        'pip',
        'PyYAML',
        'Werkzeug',
        'Jinja2',
        'pymongo',
        'Pillow',
        'ExifRead',
        'python-magic',
        'htmlmin',
        'requests',
        'lxml',
        'pytz',
        'frozendict',
        'redis',
        'uwsgi',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=find_packages(),
    package_data={
        '': ['*.*']
    }
)
