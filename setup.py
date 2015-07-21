import sys, re
from os import walk, path
from setuptools import setup, find_packages

__version = '0.2.1'


def find_package_data():
    r = {}
    for pkg in find_packages():
        r[pkg] = []
        pkg_dir = path.sep.join(pkg.split('.'))
        for root, dir_name, files in walk(pkg_dir):
            for file_name in files:
                sub_path = re.sub('^{}{}'.format(pkg_dir, path.sep), '', path.join(root, file_name))
                if re.match('res\/', sub_path):
                    r[pkg].append(sub_path)
    return r


setup(
    name='PytSite',
    version=__version,
    description='The Simple Web Framework',
    url='https://github.com/ashep/pytsite',
    download_url='https://github.com/ashep/pytsite/archive/{}.tar.gz'.format(__version),
    author='Alexander Shepetko',
    author_email='a@shepetko.com',
    license='MIT',
    install_requires=[
        'PyYAML',
        'Werkzeug',
        'Jinja2',
        'pylibmc',
        'beaker',
        'pymongo',
        'webassets',
        'Pillow',
        'ExifRead',
        'python-magic',
        'htmlmin',
        'rjsmin',
        'cssutils',
        'requests',
        'requests_oauthlib',
        'twython',
    ],
    classifiers= [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=find_packages(),
    package_data=find_package_data(),
)
