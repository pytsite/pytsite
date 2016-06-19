# PytSite Authentication HTTP API
Перед изучением этого документа убедитесь, что разобрались с 
общими правилами выполнения запросов к [HTTP API](../../../../http_api/doc/ru/index.md).

## POST pytsite.auth/sign_in
Выполняет аутентификацию пользователя.
 
### Аргументы
* **Optional** `driver: <str>`. Имя драйвера аутентификации. В случае отсутствия аргумента будет использован драйвер по 
  умолчанию.
* **Optional** `access_token_ttl: <int>`. Время жизни токена доступа в секундах. Значение по умолчанию: 3600.
* **Required** аргументы драйвера аутентификации.

### Поля ответа
* `access_token: <str>`. Токен доступа.

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


## GET pytsite.auth/access_token_info
Возвращает информацию о токене доступа.

### Аргументы
* **Required** `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`.

### Поля ответа
* `uid: <str>`: уникальный идентификатор учётной записи, к которой относится токен.
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
    "uid": "576563ef523af52badc5beac",
    "ttl": 3600,
    "expires": 3421
}
```


## GET pytsite.auth/user
Возвращает информацию об учётной записи пользователя.

### Аргументы

* **Optional** `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`. Если не указан, 
запрос будет выполняться от имени анонимной учётной записи.
* **Optional** `uid: <str>`. UID учётной записи, информацию о которой необходимо получить. Если не указан, будет 
использоваться учётная запись, от имени которой выполняется запрос, то есть, в этом случа передача аргумента 
`access_token` является обязательной. 

**При выполнении данного запроса обязательно передавать как минимум один из двух аргументов.**


### Поля ответа
Поля, возвращаемые всегда:

* `uid: <str>`. Уникальный идентификатор учётной записи.

Поля, возвращаемые в случае, если `profile_is_public` возвращаемой учётной записи равно `True`:

* `profile_url: <str>`. URL профиля учётной записи.
* `nickname: <str>`. Никнейм.
* `picture: <dict>`. Юзерпик.
    * `url: <str>`. URL.
    * `width: <int>`. Ширина в пикселях.
    * `height: <int>`. Высота в пикселях.
    * `length: <int>`. Размер в байтах.
    * `mime: <str>`. MIME-тип.
* `first_name: <str>`. Имя.
* `last_name: <str>`. Фамилия.
* `full_name: <str>`. Имя и фамилия.
* `birth_date: <str>`. Дата рождения в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
* `gender: <str>`. Пол. 'm' -- мальчик, 'f' -- девочка.
* `phone: <str>`. Номер телефона.
* `follows: <list[str]>`. UID учётных записей, на которые подписан пользователь.
* `followers: <list[str]>`. UID учётных записей, которые подписаны на пользователя.
* `urls: <list[str]>`. URL профилей пользователя в других местах.

Дополнительные поля, возвращаемые в случае, если запрашивающая учётная запись является администратором или владельцем 
запрашиваемой учётной записи.

* `created: <str>`. Время созания учётной записи в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
* `login: <str>`. Логин.
* `email: <str>`. Email.
* `last_sign_in: <str>`. Время последней успешной аутентификации в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28). 
* `last_activity: <str>`. Время последней активности в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
* `sign_in_count: <int>`. Общее количество успешных аутентификации.
* `status: <str>`. Статус учётной записи: 'active', 'waiting' или 'disabled'.
* `profile_is_public: <bool>`. Доступность профиля для всех пользователей.
* `roles: <list[str]>`. Назначенные роли.

### Примеры

Запрос:
```
curl -X GET 'https://test.com/api/1/pytsite.auth/user?access_token=0dc80160c916e629a712132d17880831
```

Ответ:
```
{
  "uid": "576563ef523af52badc5beac",
  "profile_url": "https://test.com/auth/profile/pupkeen",
  "nickname": "pupkeen",
  "picture": {
    "url": "https://test.com/image/resize/0/0/59/e0/0b544b26210ca43f.png",
    "width": 250,
    "height": 250,
    "length": 41233,
    "mime": "image/png"
  },
  "first_name": "Vasily",
  "last_name": "Pupkeen",
  "full_name": "Vasily Pupkeen",
  "birth_date": "Thu, 05 Jul 1984 00:00:00 +0300",
  "gender": "m",
  "phone": "+380501234567",
  "follows": [],
  "followers": [
    "576562d9523af52985715b6b"
  ]
  "urls": [
    "https://plus.google.com/+Vasyok"
  ],
  "created": "Sat, 18 Jun 2016 18:08:31 +0300",
  "login": "vasya@pupkeen.com",
  "email": "vasya@pupkeen.com",
  "last_sign_in": "Sun, 19 Jun 2016 15:58:17 +0300",
  "last_activity": "Sun, 19 Jun 2016 16:04:05 +0300",
  "sign_in_count": 14,
  "status": "active",
  "profile_is_public": true,
  "roles": [
    "user"
  ],
}
```


## GET pytsite.auth/sign_out
Удаляет ранее созданный токен доступа.

### Аргументы
* **Required** `access_token: <str>`. Токен доступа, полученный в результате вызова `pytsite.auth/sign_in`.

### Поля ответа
Отсутствуют.

### Примеры
Запрос:
```
curl -d "access_token=0dc80160c916e629a712132d17880831" 'https://test.com/api/1/pytsite.auth/sign_out'
```
