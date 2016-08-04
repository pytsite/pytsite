# PytSite HTTP API

## Запросы

Все запросы к HTTP API должны выполняться по протоколу [HTTP 1.1](https://tools.ietf.org/html/rfc2616).

URL любого запроса запроса миеет вид `/api/{VERSION}/{MODULE}/{ENDPOINT}`, где `{VERSION}` -- текущая версия API 
приложения; `{MODULE}` -- модуль, которому направляется запрос; `{ENDPOINT}` -- метод модуля. 

Каждый метод поддерживает один или более [HTTP-методов](https://tools.ietf.org/html/rfc2616#section-9), что 
должно быть описано в документации модуля. 

Для передачи аргуметов методам используется HTTP query string в URL для GET-запросов, либо тело POST-запросов, 
совместно с заголовком `Content-Type: application/x-www-form-urlencoded`.


## Ответы

HTTP API **всегда** возвращает ответ в формтае JSON. Для анализа успешности/ошибочности запросов, используйте 
возвращаемые [HTTP статус-коды](https://tools.ietf.org/html/rfc2616#section-10).

В каждый ответ включается заголовок 'PytSite-HTTP-API' с номером версии API.


## Примеры

### GET-запрос

GET запрос к модулю `pytsite.auth`, методу `access_token_info` с аргументом `access_token`:

```
curl -vX GET \
-d access_token=46e0b2e9a83ddc18e3358802c6f18a09 \
http://test.com/api/1/pytsite.auth/access_token_info
```

```
> GET /api/1/pytsite.auth/access_token_info?access_token=46e0b2e9a83ddc18e3358802c6f18a09 HTTP/1.1
> Host: test.com
> User-Agent: curl/7.49.1
> Accept: */*
```

Ответ:

```
< HTTP/1.1 200 OK
< Server: nginx
< Date: Sun, 19 Jun 2016 21:43:41 GMT
< Content-Type: application/json
< Content-Length: 65
< Connection: keep-alive
< Cache-Control: private, max-age=0, no-cache, no-store
< PytSite-HTTP-API: 1
< Pragma: no-cache
<
{"expires": 2718, "uid": "576563ef523af52badc5beac", "ttl": 3600}
```


### POST запрос

POST запрос к модулю `pytsite.auth`, конечной точке `sign_in` и аргументами `driver`, `login` и `password`:

```
curl -v \
-H "Content-Type: application/x-www-form-urlencoded" \
-d 'driver=password&login=vasya&password=123' \
"http://test.com/api/1/pytsite.auth/sign_in"
```

```
> POST /api/1/pytsite.auth/sign_in HTTP/1.1
> Host: test.com
> User-Agent: curl/7.49.1
> Accept: */*
> Content-Type: application/x-www-form-urlencoded
> Content-Length: 63
```

Ответ:

```
< HTTP/1.1 200 OK
< Server: nginx
< Date: Sun, 19 Jun 2016 22:09:03 GMT
< Content-Type: application/json
< Content-Length: 52
< Connection: keep-alive
< Cache-Control: private, max-age=0, no-cache, no-store
< PytSite-HTTP-API: 1
< Pragma: no-cache
< 
{"access_token": "46e0b2e9a83ddc18e3358802c6f18a09"}
```
