from setuptools import setup, find_packages

__version = '0.2.1'

setup(
    name='PytSite',
    version=__version,
    description='The Simple Web Framework',
    url='https://github.com/ashep/pytsite',
    download_url='https://github.com/ashep/pytsite/archive/{}.tar.gz'.format(__version),
    author='Alexander Shepetko',
    author_email='a@shepetko.com',
    packages=find_packages(),
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
    ]
)
