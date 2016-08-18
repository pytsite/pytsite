# PytSite Comments HTTP API

Перед изучением этого документа убедитесь, что разобрались с [PytSite HTTP API](../../../http_api/doc/ru/index.md).


## GET comments/settings

Получение параметров конфигурации комментариев.


### Аргументы

- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **int** `max_depth`. Максимальная глубина вложенности комментария.
- **int** `body_min_length`. Минимальная длина текста комментария.
- **int** `body_max_length`. Максимальная  длина текста комментария.
- **object** `statuses`. Возможные статусы комментария и их описания.
- **object** `permissions`. Права учётной записи.
    - **bool** `create`. Право на создание комментариев.


### Примеры

Запрос:

```
curl -X GET \
-d access_token=227912317f4439e6b5ba496f183947f8 \
http://test.com/api/1/comments/settings
```


Ответ:

```
{
    "body_min_length": 2, 
    "body_max_length": 2048,
    "max_depth": 4,
    "statuses": {
        "published": "Опубликован",
        "waiting": "На модерации",
        "spam": "Спам",
        "deleted": "Удалён"
    },
    "permissions": {
        "create": true
    }
}
```


## POST comments/comment

Добавление нового комментария.


### Аргументы

- *required* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *required* **str** `thread_uid`. Уникальный идентификатор ветки комментариев. Как правило, это URL страницы, на 
  которой будет отображаться данная ветка.
- *required* **str** `body`. Текст сообщения. HTML и лишние пробелы будут автоматически удалены. Минимальная длина по 
  умолчанию: 2 символа, максимальная длина по умолчанию: 2048 символов. Минимальная и максимальная длины вычисляются
  *после* очистки текста от лишних пробелов и HTML.
- *optional* **str** `parent_uid`. UID родительского комментария. При использовании этого параметра необходимо следить,
  чтобы не было превышения максимально-допустимой вложенности, которая по умолчанию составляет 4.
- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **str** `uid`. Уникальный идентификатор комментария.
- **str** `parent_uid`. Уникальный идентификатор родительского комментария.
- **str** `thread_uid`. Уникальный идентификатор ветки.
- **str** `status`. Статус.
- **int** `depth`. Глубина вложенности комментария.
- **str** `body`. Текст комментария.
- **object** `author`. Данные об учётной записи автора комментария.
    - **str** `uid`. Уникальный идентификатор.
    - **str** `nickname`. Никнейм.
    - **str** `full_name`. Имя и фамилия.
    - **str** `picture_url`. URL изображения.
    - **str** `profile_url`. URL профиля.
- **object** `publish_time`. Дата и время публикации.
    - **str** `w3c`. В формате W3C.
    - **str** `pretty`. В "человеческом" формате.
    - **str** `ago`. В формате "N минут/часов/etc назад". 
- **object** `permissions`. Права учётной записи.
    - **bool** `modify`. Право на удаление комментария.
    - **bool** `delete`. Право на изменение комментария.
 

### Примеры

Запрос:

```
curl -X POST \
-d access_token=227912317f4439e6b5ba496f183947f8 \
-d thread_uid=http://test.com/hello/world \
-d parent_uid=57b0b315523af525a269a02a \
-d body='Привет, Мир!' \
http://test.com/api/1/comments/comment
```


Ответ:

```
{
    "uid": "57b25223523af558d54f33ad", 
    "parent_uid": "57b0b315523af525a269a02a", 
    "thread_uid": "http://test.com/hello/world",
    "status": "published",
    "depth": 2,
    "body": "Привет, Мир!",
    "publish_time": {
        "pretty": "16 августа, 02:37",
        "w3c": "2016-08-16T02:37:07+0300",
        "ago": "Только что"
    }, 
    "author": {
        "uid": "579178ed523af5473134aed6",
        "nickname": "pupkeen", 
        "full_name": "Василий Пупкин",
        "picture_url": "http://test.com/image/resize/50/50/15/b5/8c319860b6a92a69.png", 
        "profile_url": "http://test.com/auth/profile/pupkeen"
    }, 
    "permissions": {
        "modify": true, 
        "delete": true
    }
}
```


## GET comments/comments

Получение списка комментариев.


### Аргументы

- *required* **str** `thread_uid`. Уникальный идентификатор ветки комментариев. Как правило, это URL страницы, на 
  которой будет отображаться данная ветка.
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **array[object]** `items`. Информация о комментариях. Структура какждого элемента полностью совпадает со структурой 
  ответа метода `POST comments/comment` за исключением того, что если комментарий имеет статус, отличный от `published`,
  то поля `body` и `author` будут отсутствовать.
- **object** `settings`. Параметры конфигурации комментариев. В точности совпадают с форматом ответа 
  `GET comments/settings`.  

### Примеры

Запрос:

```
curl -X GET \
-d access_token=227912317f4439e6b5ba496f183947f8 \
-d thread_uid=http://test.com/hello/world \
http://test.com/api/1/comments/comments
```


Ответ:

```
{
    "items": [
        {
            "uid": "57b25223523af558d54f33ad", 
            "parent_uid": "57b0b315523af525a269a02a", 
            "thread_uid": "http://test.com/hello/world",
            "status": "published",
            "depth": 2,
            "body": "Привет, Мир!",
            "publish_time": {
                "pretty": "16 августа, 02:37",
                "w3c": "2016-08-16T02:37:07+0300",
                "ago": "Только что"
            }, 
            "author": {
                "uid": "579178ed523af5473134aed6",
                "nickname": "pupkeen", 
                "full_name": "Василий Пупкин",
                "picture_url": "http://test.com/image/resize/50/50/15/b5/8c319860b6a92a69.png", 
                "profile_url": "http://test.com/auth/profile/pupkeen"
            }, 
            "permissions": {
                "modify": true, 
                "delete": true
            }
        }
    ]
}
```


## DELETE comments/comment

Смена статуса комментария на `deleted`.


### Аргументы

- *required* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *required* **str** `uid`. Уникальный идентификатор комментария.
- *optional* **str** `driver`. Дравйер.


### Формат ответа

Объект.

- **bool** `status`. Флаг успешности обработки запроса.


### Примеры

Запрос:

```
curl -X DELETE \
-d access_token=227912317f4439e6b5ba496f183947f8 \
-d uid=57b25223523af558d54f33ad \
http://test.com/api/1/comments/comment
```


Ответ:

```
{
    "status": true
}
```


## POST comments/report

Отправка жалобы на комментарий.


### Аргументы

- *required* **str** `uid`. Уникальный идентификатор комментария.


### Формат ответа

Объект.

- **bool** `status`. Флаг успешности обработки запроса.


### Примеры

Запрос:

```
curl -X POST \
-d uid=57b25223523af558d54f33ad \
http://test.com/api/1/comments/report
```


Ответ:

```
{
    "status": true
}
```
