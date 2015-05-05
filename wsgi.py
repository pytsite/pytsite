import pytsite.core.application as app

app.init(__file__)


def application(env, start_response):
    return app.wsgi_dispatch(env, start_response)
