from setuptools import setup, find_packages

setup(
    name='PytSite',
    version='0.0.1',
    description='Simple CMS',
    url='https://github.com/ashep/pytsite',
    author='Alexander Shepetko',
    author_email='a@shepetko.com',
    license='MIT',
    install_requires=[
        'PyYAML',
        'Werkzeug',
        'Jinja2',
        'webassets',
        'Pillow',
        'python-magic',
        'htmlmin',
    ]
)
