#!/bin/bash

REQUIRED_PKGS=(pytest pytest-cov PyYAML Werkzeug Jinja2 pylibmc beaker pymongo webassets Pillow ExifRead python-magic
               htmlmin jsmin cssmin requests requests_oauthlib twython lxml feedgen pytz)

PYTHONPATH=${PYTHONPATH}:`pwd`
export PYTHONPATH

if [ ! -d  env ]; then
    virtualenv --no-wheel ./env
    source ./env/bin/activate
    for PKG in ${REQUIRED_PKGS[*]}; do pip install ${PKG}; done
else
    source env/bin/activate
fi

cd testing
if [ ! -z ${1} ]; then
    py.test --exitfirst tests/${1}
else
    py.test --exitfirst tests
fi
