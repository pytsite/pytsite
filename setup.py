from setuptools import setup, find_packages

setup(
    name='PytSite',
    version='0.0.1',
    description='Python Web Framework',
    url='https://github.com/ashep/pytsite',
    author='Alexander Shepetko',
    author_email='a@shepetko.com',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'PyYAML',
        'Werkzeug',
        'Jinja2',
        'pymongo',
        'webassets',
        'Pillow',
        'ExifRead',
        'python-magic',
        'htmlmin',
        'rjsmin',
        'cssutils',
    ]
)
