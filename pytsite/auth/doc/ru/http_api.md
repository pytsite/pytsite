# PytSite Authentication HTTP API

Перед изучением этого документа убедитесь, что разобрались с [PytSite HTTP API](../../../http_api/doc/ru/index.md).


## POST auth/sign_in

Аутентификация учётной записи.


### Аргументы

- *optional* **str** `driver`. Имя драйвера аутентификации.
- *required* аргументы драйвера аутентификации.


### Формат ответа

Объект.

- **str** `access_token`. Токен доступа.


### Примеры

Запрос. В данном примере аргументы `login` и `password` являются аргументами драйвера `password`:

```
curl \
-d driver=password \
-d login=vasya@pupkeen.com \
-d password=Very5tr0ngP@ssw0rd \
https://test.com/api/1/auth/sign_in
```


Ответ:

```
{
    "access_token": "0dc80160c916e629a712132d17880831"
}
```


## GET auth/access_token_info

Получение информации о токене доступа.


### Аргументы
- *required* **str** `access_token`. Токен доступа.


### Фомат ответа

Объект.

- **str** `uid`. Уникальный идентификатор учётной записи, к которой относится токен.
- **int** `ttl`. Время жизни токена в секундах.


### Примеры

Запрос:

```
curl -X GET \
-d access_token=0dc80160c916e629a712132d17880831 \
https://test.com/api/1/auth/access_token_info
```

Ответ:

```
{
    "uid": "576563ef523af52badc5beac",
    "ttl": 3600
}
```


## GET auth/user

Информация об учётной записи пользователя.


### Аргументы

**При выполнении данного запроса обязательно передавать как минимум один из двух аргументов.**

- *optional* **str** `access_token`. Токен доступа, полученный в результате вызова `auth/sign_in`. Если не 
  указан, запрос будет выполняться от имени анонимной учётной записи.
- *optional* **str** `uid`. UID учётной записи, информацию о которой необходимо получить. Если не указан, будет 
  использоваться учётная запись, от имени которой выполняется запрос, то есть, в этом случа передача аргумента 
  `access_token` является обязательной. 


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
- **str** `birth_date`. Дата рождения в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
- **str** `gender`. Пол. 'm' -- мальчик, 'f' -- девочка.
- **str** `phone`. Номер телефона.
- **array[str]** `follows`. UID учётных записей, на которые подписан пользователь.
- **array[str]** `followers`. UID учётных записей, которые подписаны на пользователя.
- **array[str]** `urls`. URL профилей пользователя в других местах.

Дополнительные поля, возвращаемые в случае, если запрашивающая учётная запись является администратором или владельцем 
запрашиваемой учётной записи.

- **str** `created`. Время созания учётной записи в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
- **str** `login`. Логин.
- **str** `email`. Email.
- **str** `last_sign_in`. Время последней успешной аутентификации в формате 
  [RFC822](https://www.w3.org/Protocols/rfc822/#z28). 
- **str** `last_activity`. Время последней активности в формате [RFC822](https://www.w3.org/Protocols/rfc822/#z28).
- **int** `sign_in_count`. Общее количество успешных аутентификации.
- **str** `status`. Статус учётной записи: 'active', 'waiting' или 'disabled'.
- **bool** `profile_is_public`. Доступность профиля для всех пользователей.
- **array[str]** `roles`. UID назначенных ролей.

Также возможно добавление дополнительных полей сторонними модулями.


### Примеры

Запрос:

```
curl -X GET \
-d access_token=0dc80160c916e629a712132d17880831 \
https://test.com/api/1/auth/user
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
  "followers":
  [
      "576562d9523af52985715b6b"
  ],
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


## POST auth/sign_out

Удаление ранее выданного токена доступа.


### Аргументы

- *required* **str** `access_token`. Токен доступа.


### Формат ответа

Метод не возвращает данных.


### Примеры

Запрос:

```
curl -d access_token=0dc80160c916e629a712132d17880831 https://test.com/api/1/auth/sign_out
```
