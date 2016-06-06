# PytSite Auth HTTP API

## POST /api/{VERSION}/pytsite.auth/sign_in
Выполняет аутентификацию пользователя и возвращает токен доступа.
 
### Аргументы
* Optional `driver: <str>`. Имя драйвера аутентификации. В случае отсутствия аргумента будет использован драйвер по 
  умолчанию.
* Optional `access_token_ttl: <int>`. Время жизни токена доступа в секундах. Значение по умолчанию: 3600.
* Аргументы драйвера аутентификации.

### Поля ответа
* `access_token: <str>`: токен доступа.

### Примеры
Запрос:
```
curl \
-d "driver=password" \
-d "access_token_ttl=86400" \
-d "login=vasya@pupkeen.com" \
-d "password=Very5tr0ngP@ssw0rd" \
'https://test.com/api/1/pytsite.auth/sign_in'
```

Ответ:
```
{
    "access_token": "0dc80160c916e629a712132d17880831"
}
```


## GET /api/{VERSION}/pytsite.auth/access_token_info
Возвращает информацию о токене доступа.

### Аргументы
* Required `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`.

### Поля ответа
* `login: <str>`: содержимое поля 'login' учётной записи.
* `ttl: <int>`: начальное время жизни токена в секундах.
* `expires: <int>`: оставшееся время жизни токена в секундах.

### Примеры

Запрос:
```
curl -X GET 'https://test.com/api/1/pytsite.auth/access_token_info?access_token=0dc80160c916e629a712132d17880831'
```

Ответ:
```
{
    "login": "vasya@pupkeen.com",
    "ttl": 3600,
    "expires": 3421
}
```


## GET /api/{VERSION}/pytsite.auth/user
Возвращает информацию об учётной записи пользователя.

### Аргументы
* Required `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`.
* Optional `fields: <list>`. Поля учётной записи, содержимое которых необходимо вернуть в ответе.

### Поля ответа
* `login: <str>`: содержимое поля 'login' учётной записи.
* `<list>`: содержимое полей учётной записи, перечисленных в аргументе `fields`.

### Примеры
Запрос:
```
curl -X GET 'https://test.com/api/1/pytsite.auth/user?\
access_token=0dc80160c916e629a712132d17880831&\
fields=first_name,last_name,nickname,picture.url'
```

Ответ:
```
{
    "login": "vasya@pupkeen.com",
    "first_name": "Pupkeen",
    "last_name": "Vasya",
    "nickname": "vasyok",
    "picture": {
        "url": "https://test.com/image/resize/0/0/72/93/7981f8c6efdea4f4.png"
    }
}
```


## GET /api/{VERSION}/pytsite.auth/sign_out
Удаляет ранее созданный токен доступа.

### Аргументы
* Required `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`.

### Поля ответа
Отсутствуют.

### Примеры
Запрос:
```
curl -d "access_token=0dc80160c916e629a712132d17880831" 'https://test.com/api/1/pytsite.auth/sign_out'
```
