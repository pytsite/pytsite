import re, json
from os import walk, path, system
from setuptools import setup, find_packages, Command

with open(path.join(path.dirname(__file__), 'pytsite', 'pytsite.json')) as f:
    data = json.load(f)
    pkg_name = data['name'].lower()
    pkg_version = data['version']
    pkg_description = data['description']['en']
    pkg_url = data['url']
    pkg_author = data['author']['name']
    pkg_author_email = data['author']['email']
    pkg_license = data['license']['name']

ASSET_FNAME_RE = re.compile('\.(png|jpg|jpeg|gif|svg|ttf|woff|woff2|eot|otf|map|js|css|less|txt|md|yml|jinja2|json)$')


class CleanCommand(Command):
    """Custom clean command to tidy up the project root.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        system('rm -vrf ./build ./dist')


def find_package_data():
    r = {}

    for pkg in find_packages():
        pkg_path = path.sep.join(pkg.split('.'))
        for root, dir_name, files in walk(pkg_path):
            for file_name in files:
                if ASSET_FNAME_RE.search(file_name):
                    if pkg not in r:
                        r[pkg] = []
                    file_ext = path.splitext(file_name)[1]
                    path_glob = re.sub('^{}{}'.format(pkg_path, path.sep), '', path.join(root, '*' + file_ext))
                    if path_glob not in r[pkg]:
                        r[pkg].append(path_glob)

    return r


setup(
    name=pkg_name,
    version=pkg_version,
    description=pkg_description,
    url=pkg_url,
    author=pkg_author,
    author_email=pkg_author_email,
    license=pkg_license,
    download_url='https://github.com/pytsite/pytsite/archive/{}.tar.gz'.format(pkg_version),
    install_requires=[
        'PyYAML',
        'Werkzeug',
        'Jinja2',
        'pymongo',
        'Pillow',
        'ExifRead',
        'python-magic',
        'htmlmin',
        'jsmin',
        'requests',
        'lxml',
        'pytz',
        'frozendict',
        'uwsgi',
        'dateparser'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Natural Language :: Ukrainian',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=find_packages(),
    package_data=find_package_data(),
    cmdclass={
        'clean': CleanCommand,
    }
)

