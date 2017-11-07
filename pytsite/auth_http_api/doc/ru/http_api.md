# PytSite Authentication HTTP API version 2


## POST auth/access-token/:driver

Создание токена доступа.


### Аргументы

- `driver`: имя драйвера аутентификации.


### Параметры

- *required* аргументы драйвера аутентификации.


### Формат ответа

Объект.

- **str** `token`. Токен доступа.
- **str** `user_uid`. Идентификатор владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Получение токена доступа через драйвер 'password'. Параметры `login` и
`password` являются аргументами драйвера:

```
curl -X POST \
-d login='vasya@pupkeen.com' \
-d password='Very5tr0ngP@ssw0rd' \
https://test.com/api/2/auth/access-token/password
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
- **str** `user_uid`. Идентификатор владельца токена доступа.
- **int** `ttl`. Срок действия токена доступа в секундах.
- **str** `created`. Время создания токена доступа в формате W3C.
- **str** `expires`. Время истечения токена доступа в формате W3C.


### Примеры

Запрос:

```
curl -X GET https://test.com/api/2/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
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

Удаление токена доступа.


### Аргументы

- `token`. Токен доступа.


### Формат ответа

Метод **всегда** возвращает объект вида `{status: true}`.


### Примеры

Запрос:

```
curl -X DELETE https://test.com/api/2/auth/access-token/e51081bc4632d8c2a31ac5bd8080af1b
```


Ответ:

```
{
  "status": true
}
```


## GET /auth/is_anonymous

Проверка, является ли текущая учётная запись авторизованной.


### Формат ответа

Объект.

- **bool** `status`. Результат проверки.


### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/2/auth/is_anonymous
```

Ответ:

```
{
  "status": true
}
```


## GET auth/user/:uid

Получение информации об учётной записи.


### Аргументы

- `uid`. Идентификатор учётной записи.


### Формат ответа

Объект.

Поля, возвращаемые всегда:

- **str** `uid`. Идентификатор учётной записи.

Поля, возвращаемые в случае, если `profile_is_public` возвращаемой
учётной записи равен `true`, запрашивающая учётная запись запись
является  администратором или владельцем запрашиваемой учётной записи:

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
- **str** `full_name`. Полное имя.
- **str** `birth_date`. Дата рождения в формате W3C.
- **str** `gender`. Пол: 'm' -- мальчик, 'f' -- девочка.
- **str** `phone`. Номер телефона.
- **array\[str\]** `urls`. URL профилей учётной записи в других местах.
- **int** `follows_count`. Количество учётных записей, на которые
  подписан пользователь.
- **int** `followers_count`. Количество учётных записей, которые
  подписаны на пользователя.
- **bool** `is_followed`. Является ли учётная запись, выполняющая
  запрос, подписчиком учётной записи.
- **bool** `is_follows`. Является ли учётная запись подписчиком учётной
  записи, выполняющей запрос.

Дополнительные поля, возвращаемые в случае, если запрашивающая учётная
запись является администратором или владельцем запрашиваемой учётной
записи.

- **str** `created`. Время создания учётной записи в формате W3C.
- **str** `login`. Логин.
- **str** `email`. Email.
- **str** `last_sign_in`. Время последней успешной аутентификации в
  формате W3C.
- **str** `last_activity`. Время последней активности в формате W3C.
- **int** `sign_in_count`. Общее количество успешных аутентификаций.
- **str** `status`. Статус учётной записи: 'active', 'waiting' или
  'disabled'.
- **bool** `profile_is_public`. Видимость профиля.

Также возможно добавление дополнительных полей сторонними модулями.


### Примеры

Запрос:

```
curl -X GET \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \  
https://test.com/api/2/auth/user/576563ef523af52badc5beac
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
  "profile_is_public": true
}
```


## GET auth/users

Получение информации об учётных записях.


### Параметры

- *required* **array\[str\]** `uids`. Идентификаторы учётных записей.


### Формат ответа

Массив объектов. Формат каждого объекта идентичен ответу
**GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X GET \
-d uids='["590ed572523af516d789a063", "590ed5f3523af516d789a0cd"]' \
https://test.com/api/2/auth/users
```


Ответ:

```
[
  {
    "uid": "590ed572523af516d789a063",
    ...
  },
  {
    "uid": "590ed5f3523af516d789a0cd",
    ...
  }
]
```


## PATCH auth/user/:uid

Изменение учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи.


### Параметры

- **str** `email`. Адрес электронной почты.
- **str** `nickname`. Никнейм.
- **str** `picture`. UID изображения.
- **str** `first_name`. Имя.
- **str** `last_name`. Фаимлия.
- **str** `description`. Описание.
- **str** `birth_date`. Дата рождения в формате W3C.
- **str** `gender`. Пол: `m` -- мальчик, `f` -- девочка.
- **str** `phone`. Номер телефона.
- **str** `country`. Страна.
- **str** `city`. Город.
- **array\[str\]** `urls`. URL профилей учётной записи в других местах.
- **bool** `profile_is_public`. Видимость профиля для всех.


### Формат ответа

Идентичен **GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
-d email=hello@world.com \
-d first_name=Hello \
-d last_name=World \
-d gender=f \
-d profile_is_public=false \
-d description='I am an invisible girl' \
https://test.com/api/2/auth/user/576563ef523af52badc5beac
```


## GET auth/following_count/:uid

Получения количества подписчиков учётной записи и количества
учётных записей, на которых данная учётная запись подписана.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи.


### Формат ответа

- **int** `follows`. Количество учётных записей, подписчиком которых
  является запрашивающая учётная запись.
- **int** `followers`. Количество подписчиков запрашивающей учётной
  записи.


## GET auth/follows/:uid

Получение учётной записи, фолловером которых является данная учётная
запись.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи.


### Параметры

- **int** `skip`. Смещение.
- **int** `count`. Количество элементов в ответе. Значение по
  умолчанию: 10. Минимальное значение: 1. Максимальное значение: 100.


### Формат ответа

- **int** `remains`. Количество оставшихся элементов.
- **array\[object\]** `result`. Данные учётныъ записей. Формат каждого
  элемента идентичен **GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
-d skip=100 \
-d count=50 \
https://test.com/api/2/auth/follows/576563ef523af52badc5beac
```


Ответ:

```
{
  "remains": 768,
  "result":
  [
    {
        "uid": "589ec1ba523af557a2099b5f",
        ...
    },
    ...
  ]
}
```


## GET auth/followers/:uid

Получение списка фолловеров учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи.


### Параметры

- **int** `skip`. Смещение.
- **int** `count`. Количество элементов в ответе. Значение по
  умолчанию: 10. Минимальное значение: 1. Максимальное значение: 100.


### Формат ответа

- **int** `remains`. Количество оставшихся элементов.
- **array\[object\]** `result`. Данные учётной записи. Формат каждого
  элемента массива идентичен **GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
-d skip=7 \
-d count=14 \
https://test.com/api/2/auth/followers/589ec1ba523af557a2099b5f
```


Ответ:

```
{
  "remains": 3,
  "result":
  [
    {
        "uid": "576563ef523af52badc5beac",
        ...
    },
    ...
  ]
}
```


## POST auth/follow/:uid

Фолловинг учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи для фолловинга.


### Формат ответа

Объект.

- **bool** `status`. Результат выполнения операции


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/2/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
  "status": true
}
```


## DELETE auth/follow/:uid

Анфолловинг учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи для анфолловинга.


### Формат ответа

Объект.

- **bool** `status`. Результат выполнения операции


### Примеры

Запрос:

```
curl -X DELETE \ 
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/2/auth/follow/576563ef523af52badc5beac
```

Ответ:

```
{
  "status": true
}
```


## GET auth/blocked_users/:uid

Получение списка заблокированных учётных записей.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор учётной записи.


### Параметры

- **int** `skip`. Смещение.
- **int** `count`. Количество элементов в ответе. Значение по
  умолчанию: 10. Минимальное значение: 1. Максимальное значение: 100.


### Формат ответа

- **int** `remains`. Количество оставшихся элементов.
- **array\[object\]** `result`. Данные учётных записей. Формат каждого
  элемента массива идентичен **GET auth/user/:uid**.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
-d skip=7 \
-d count=14 \
https://test.com/api/2/auth/blocked_users/589ec1ba523af557a2099b5f
```


Ответ:

```
{
  "remains": 3,
  "result":
  [
    {
        "uid": "576563ef523af52badc5beac",
        ...
    },
    ...
  ]
}
```



## POST auth/block_user/:uid

Блокировка учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор блокируемой учётной записи.


### Формат ответа

- **bool** `status`. Результат выполнения операции


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/2/auth/block_user/576563ef523af52badc5beac
```

Ответ:

```
{
  "status": true
}
```


## DELETE auth/block_user/:uid

Отмена блокировки учётной записи.
Обязательна [аутентификация](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#Аутентификация-запросов).


### Аргументы

- `uid`. Идентификатор заблокированной учётной записи.


### Формат ответа

- **bool** `status`. Результат выполнения операции


### Примеры

Запрос:

```
curl -X DELETE \
-H 'PytSite-Auth: e51081bc4632d8c2a31ac5bd8080af1b' \
https://test.com/api/2/auth/block_user/576563ef523af52badc5beac
```

Ответ:

```
{
  "status": true
}
```
