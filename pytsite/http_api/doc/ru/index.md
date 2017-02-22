# PytSite HTTP API

## Запросы

Все запросы к HTTP API должны выполняться по протоколу [HTTP 1.1](https://tools.ietf.org/html/rfc2616).

URL любого запроса запроса миеет вид `/api/{VERSION}/{ENDPOINT}`, где `{VERSION}` -- версия API; `{ENDPOINT}` -- 
конечная точка.

Каждая конечная точка поддерживает один или более [HTTP-методов](https://tools.ietf.org/html/rfc2616#section-9), что 
должно быть описано в документации соответствующего модуля. 

Каждая конечная точка может принимать **аргументы** и **параметры**. **Аргументы** передаются как часть URL, а 
параметры -- при помощи HTTP query string для GET-запросов, либо внтури тела POST-запросов, совместно с заголовком 
`Content-Type: application/x-www-form-urlencoded`.


## Ответы

HTTP API **всегда** возвращает ответ в формтае JSON. Для анализа успешности/ошибочности запросов, используйте 
возвращаемые [HTTP статус-коды](https://tools.ietf.org/html/rfc2616#section-10).

В каждый ответ включается заголовок 'PytSite-HTTP-API', содержащий номер версии API, которая обработала запрос.


## Аутентификация запросов

Запросы к некоторым точкам могут требовать предварительной аутентификации. Для этого используется значение 
HTTP-заголовка `PytSite-Auth`, которое должно содержать [токен доступа](../../../auth/doc/ru/http_api.md) учётной 
записи.

Пример:

```
curl -H 'PytSite-Auth: b81de38b9b9589f9a0ec569416e75a25' http://test.com/api/1/hello/world
```

```
> GET /api/1/hello/world HTTP/1.1
> Host: test.com
> User-Agent: curl/7.52.1
> Accept: */*
> PytSite-Auth: 34f99b827cf151ecfc1bf6811ed7e82c
```


## Аутентификация запросов при помощи cookies

Для веб-приложений иногда может быть удобно использовать cookie. Для этого используется cookie **PYTSITE_SESSION** со 
значением, полученным от PytSite со стороны сервера после успешной аутентификации через web-форму. 


## Переключение локализации запросов

В случае, если приложение поддерживает более одного языка, в некоторых случаях при выполнении запросов может возникать 
необходимость переключения локализации. Для этого используется заголовок `PytSite-Lang`.
  
Пример:

```
curl -H 'PytSite-Lang: uk' http://test.com/api/1/hello/world
```

```
> GET /api/1/hello/world HTTP/1.1
> Host: test.com
> User-Agent: curl/7.52.1
> Accept: */*
> PytSite-Lang: uk
```


## Примеры

GET-запрос к конечной точке **hello/:arg** c аргументом **arg** равным  *'world'* и параметром **param** равным 
*'beautiful'*.

```
curl -v -X GET -d param=beautiful http://test.com/api/1/hello/world
```

```
> GET /api/1/hello/world?param=beautiful HTTP/1.1
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
...
```


POST-запрос к конечной точке `auth/access-token/:driver` с аргументом **driver** равным *'password'*, параметрами 
**login** равным *'vasya'* и **password** равным *'123'*.

```
curl -v -X POST -d login=vasya -d password=123 http://test.com/api/1/auth/access-token/password
```

```
> POST /api/1/auth/access-token/password HTTP/1.1
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
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```
