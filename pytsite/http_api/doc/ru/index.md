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


## Общие параметры для всех запросов

- *optional* **str** `language`. Переключение локализации. В качестве значения параметра ожидается двухбуквенный код 
  языка, поддерживаемый системой. то есть определённый в параметре конфигурации `languages`.
- *optional* **str** `access_token`. Авторизация запроса. В качестве значения параметра ожидается строка, содержащая 
  токен доступа, полученный при помощи POST-запроса к точке [auth/access-token](../../../auth/doc/ru/http_api.md). 
  При получении данного параметра будет выполнена попытка аутентификации учётной записи, соответствующей полученному 
  токену.   


## Ответы

HTTP API **всегда** возвращает ответ в формтае JSON. Для анализа успешности/ошибочности запросов, используйте 
возвращаемые [HTTP статус-коды](https://tools.ietf.org/html/rfc2616#section-10).

В каждый ответ включается заголовок 'PytSite-HTTP-API', содержащий номер версии API, которая обработала запрос.


## Примеры

GET-запрос к конечной точке **auth/access-token/:token** c аргументом **token** со значеним 
*'46e0b2e9a83ddc18e3358802c6f18a09'* и параметром **language** со значением *'ru'*.

```
curl -v -X GET 
-d language=ru \
http://test.com/api/1/auth/access-token/46e0b2e9a83ddc18e3358802c6f18a09
```

```
> GET /api/1/auth/access-token/46e0b2e9a83ddc18e3358802c6f18a09?language=ru HTTP/1.1
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
{
    "token": "46e0b2e9a83ddc18e3358802c6f18a09",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


POST-запрос к конечной точке `auth/access-token/:driver` с аргументом **driver** со значением *'password'*, параметрами 
**language** со значением *'ru'*, **login** со значением *'vasya'* и **password** со значением *'123'*.

```
curl -v -X POST \
-d language=ru \
-d login=vasya \
-d password=123 \
http://test.com/api/1/auth/access-token/password
```

```
> POST /api/1/auth/sign_in HTTP/1.1
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
