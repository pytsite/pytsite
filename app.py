import pytsite.core.application as app

app.init(__file__)

from pytsite.core import lang


print(lang.trans('app@test'))
print(lang.trans('app@test'))
print(lang.trans('app@test'))

app.console_dispatch()