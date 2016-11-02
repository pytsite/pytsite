# PytSite ODM HTTP API

## GET odm/entity

Получение сущности.


### Аргументы

- *required* **str** `model`. Модель.
- *required* **str** `uid`. UID сущности.
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md).


### Формат ответа

Объект.


### Примеры

Запрос:

```
curl -X GET \
-d model=product \
-d uid=580243983e7d899753249cec \
http://test.com/api/1/odm/entity
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Картошка",
    "description": "Очень вкусный и полезный продукт."
}
```


## POST odm/entity

Создание сущности.


### Аргументы

- *required* **str** `model`. Модель.
- *required* **object**. Поля сущности.
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md).


### Формат ответа

Объект.


### Примеры

Запрос:

```
curl -X POST \
-d model=product \
-d title=Картошка \
-d description='Очень вкусный и полезный продукт.' \
http://test.com/api/1/odm/entity
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Картошка",
    "description": "Очень вкусный и полезный продукт."
}
```


## PATCH odm/entity

Изменение сущности.


### Аргументы

- *required* **str** `model`. Модель.
- *required* **str** `uid`. UID сущности.
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md).
- *required* **object**. Поля сущности.


### Примеры

Запрос:

```
curl -X PATCH \
-d model=product \
-d uid=580243983e7d899753249cec \
-d title='Уже не картошка' \
-d description='Это теперь капуста!' \
http://test.com/api/1/odm/entity
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Уже не картошка",
    "description": "Это теперь капуста!"
}
```


## DELETE odm/entity

Удаление сущностей.


### Аргументы

- *required* **str** `model`. Модель.
- *required* **str** `uid`. UID сущностей.
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md).
