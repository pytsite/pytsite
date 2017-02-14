# PytSite ODM HTTP API


## POST odm/entity/:model

Создание сущности.


### Аргументы

- `model`. Модель.


### Параметры

- *required* поля сущности.


### Формат ответа

Объект, содержащий поля сущности и их значения.


### Примеры

Запрос:

```
curl -X POST \
-d title='Картошка' \
-d description='Очень вкусный и полезный продукт.' \
http://test.com/api/1/odm/entity/product
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Картошка",
    "description": "Очень вкусный и полезный продукт."
}
```


## GET odm/entity/:model/:uid

Получение сущности.


### Аргументы

- `model`. Модель.
- `uid`. UID.


### Формат ответа

Полностью совпадает с форматом ответа **POST odm/entity/:model**.


### Примеры

Запрос:

```
curl -X GET http://test.com/api/1/odm/entity/product/580243983e7d899753249cec
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Картошка",
    "description": "Очень вкусный и полезный продукт."
}
```


## PATCH odm/entity/:model/:uid

Изменение сущности.


### Аргументы

- `model`. Модель.
- `uid`. UID.


### Параметры

- *required* поля сущности, которые необходимо изменить.


### Формат ответа

Полностью совпадает с форматом ответа **POST odm/entity/:model**.


### Примеры

Запрос:

```
curl -X PATCH \
-d title='Уже не картошка' \
-d description='Это теперь капуста!' \
http://test.com/api/1/odm/entity/product/580243983e7d899753249cec
```


Ответ:

```
{
    "uid": "580243983e7d899753249cec",
    "title": "Уже не картошка",
    "description": "Это теперь капуста!"
}
```


## DELETE odm/entity/:model/:uid

Удаление сущности.


### Аргументы

- *required* **str** `model`. Модель.
- *required* **str** `uid`. UID сущности.


### Формат ответа

Объект.

- **bool** `status`. Результат обработки запроса.


### Примеры

Запрос:

```
curl -X DELETE http://test.com/api/1/odm/entity/product/580243983e7d899753249cec
```


Ответ:

```
{
    "status": true
}
```
