# PytSite Authentication HTTP API


## POST auth/access-token/:driver

Создание токена доступа.


### Аргументы

- `driver`: имя драйвера аутентификации.


### Параметры

- *required* аргументы драйвера аутентификации.


### Формат ответа

Объект.

- **str** `token`. Токен доступа.
- **str** `user_uid`. Идентификатор учётной записи владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Получение токена доступа через драйвер 'password'. Параметры `login` и `password` являются аргументами драйвера:

```
curl -X POST \
-d login=vasya@pupkeen.com \
-d password=Very5tr0ngP@ssw0rd \
https://test.com/api/1/auth/access-token/password
```


Ответ:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


## GET auth/access-token/:token

Получение информации о токене доступа.


### Аргументы

- `token`. Токен доступа.


### Фомат ответа

Объект.

- **str** `token`. Токен доступа.
- **str** `user_uid`. Идентификатор учётной записи владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Запрос:

```
curl -X GET https://test.com/api/1/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
```

Ответ:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```


## DELETE auth/access-token/:token

Удаление ранее созданного токена доступа.


### Аргументы

- `token`. Токен доступа.


### Формат ответа

В случае отсутствия ошибок метод всегда возвращает объект вида `{status: true}`.


### Примеры

Запрос:

```
curl -X DELETE https://test.com/api/1/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
```


Ответ:

```
{
  "status": true
}
```



## GET auth/user/:uid

Получение информации об учётной записи пользователя.


### Аргументы

- `uid`. Уникальный идентификатор учётной записи.


### Формат ответа

Объект.

Поля, возвращаемые всегда:

- **str** `uid`. Уникальный идентификатор учётной записи.

Поля, возвращаемые в случае, если `profile_is_public` возвращаемой учётной записи равен `true`, запрашивающая учётная 
запись является администратором или владельцем запрашиваемой учётной записи:

- **str** `profile_url`. URL профиля учётной записи.
- **str** `nickname`. Никнейм.
- **object** `picture`. Юзерпик.
    - **str** `url`. URL.
    - **int** `width`. Ширина в пикселях.
    - **int** `height`. Высота в пикселях.
    - **int** `length`. Размер в байтах.
    - **str** `mime`. MIME-тип.
- **str** `first_name`. Имя.
- **str** `last_name`. Фамилия.
- **str** `full_name`. Имя и фамилия.
- **str** `birth_date`. Дата рождения в формате W3C.
- **str** `gender`. Пол. 'm' -- мальчик, 'f' -- девочка.
- **str** `phone`. Номер телефона.
- **array[str]** `follows`. UID учётных записей, на которые подписан пользователь.
- **int** `follows_count`. Количество учётных записей, на которые подписан пользователь.
- **array[str]** `followers`. UID учётных записей, которые подписаны на пользователя.
- **int** `followers_count`. Количество учётных записей, которые подписаны на пользователя.
- **bool** `is_followed`. Является ли учётная запись, выполняющая запрос, подписчиком пользователя.
- **bool** `is_follows`. Является ли пользователь подписчиком учётной записи, выполняющей запрос.
- **array[str]** `urls`. URL профилей пользователя в других местах.

Дополнительные поля, возвращаемые в случае, если запрашивающая учётная запись является администратором или владельцем 
запрашиваемой учётной записи.

- **str** `created`. Время созания учётной записи в формате W3C.
- **str** `login`. Логин.
- **str** `email`. Email.
- **str** `last_sign_in`. Время последней успешной аутентификации в формате W3C. 
- **str** `last_activity`. Время последней активности в формате W3C.
- **int** `sign_in_count`. Общее количество успешных аутентификаций.
- **str** `status`. Статус учётной записи: 'active', 'waiting' или 'disabled'.
- **bool** `profile_is_public`. Доступность профиля для всех пользователей.
- **array[str]** `roles`. UID назначенных ролей.

Также возможно добавление дополнительных полей сторонними модулями.


### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \  
https://test.com/api/1/auth/user/576563ef523af52badc5beac
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
  "birth_date": "1984-07-05T11:19:18+0300",
  "gender": "m",
  "phone": "+380501234567",
  "follows": [],
  "follows_count": 0,
  "followers":
  [
      "576562d9523af52985715b6b"
  ],
  "followers_count": 1,
  "urls":
  [
      "https://plus.google.com/+Vasyok"
  ],
  "created": "2010-03-17T11:19:18+0300",
  "login": "vasya@pupkeen.com",
  "email": "vasya.p@gmail.com",
  "last_sign_in": "2016-09-12T01:22:56+0300",
  "last_activity": "2016-09-12T11:19:18+0300",
  "sign_in_count": 14,
  "status": "active",
  "profile_is_public": true,
  "roles":
  [
      "57d665063e7d8960ed762231"
  ]
}
```


## PATCH auth/user/:uid

Изменение учётной записи пользователя. Обязательна авторизация

### Аргументы

- `uid`. Уникальный идентификатор учётной записи.


### Параметры

- **object** изменяемые поля:
    - **str** `email`.
    - **str** `nickname`.
    - **str** `picture`.
    - **str** `first_name`.
    - **str** `last_name`.
    - **str** `description`.
    - **str** `birth_date`.
    - **str** `gender`.
    - **str** `phone`.
    - **str** `country`.
    - **str** `city`.
    - **array[str]** `urls`.
    - **bool** `profile_is_public`.


## POST auth/follow/:uid

Фолловинг пользователя. Обязательна авторизация.


### Аргументы

- `uid`. Уникальный идентификатор учётной записи для фолловинга.


### Формат ответа

Объект.

- **array** `follows`. Список UID учётных записей, фолловером которых является учётная запись, выполнявшая запрос.


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
    "follows": ["576563ef523af52badc5beac"]
}
```


## DELETE auth/follow/:uid

Анфолловинг пользователя. Обязательна авторизация. 


### Аргументы

- `uid`. Уникальный идентификатор учётной записи для анфолловинга.


### Формат ответа

Объект.

- **array** `follows`. Список UID учётных записей, фолловером которых является учётная запись, выполнявшая запрос.


### Примеры

Запрос:

```
curl -X DELETE \ 
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/1/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
    "follows": []
}
```
