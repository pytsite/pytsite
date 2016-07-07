# PytSite Image HTTP API

Перед изучением этого документа убедитесь, что разобрались с [PytSite HTTP API](../../../http_api/doc/ru/index.md).


## POST pytsite.image/file

Загрузка изображения. Для работы с этим методом **должен** использоваться 
[HTTP Multipart Content-Type](https://www.ietf.org/rfc/rfc2388.txt)


### Аргументы

- *required* **binary** `file{N}`. Загружаемый файл, где `{N}` -- порядковый номер файла.  
- *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).


### Формат ответа

Массив объектов.

- **str** `uid`. Уникальный идентификатор изображения.


### Примеры

Запрос:

```
curl -v \
-F access_token=b81de38b9b9589f9a0ec569416e75a25 \
-F file1=@/home/user/Documents/HelloWorld.jpg \
-F file2=@/home/user/Documents/HereWeGo.png \
http://test.com/api/1/pytsite.image/file
```

Ответ:

```
[
    {"uid": "5775fa3b523af5338fe839f3"},
    {"uid": "5775fa3b523af5338fe839f4"}
]
```


## GET pytsite.image/file

Получение информации об изображении.


### Аргументы

* *required* **str** `uid`. Уникальный идентификатор изображения.  
* *optional* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
* *optional* **int** `thumb_width`. Ширина изображения предварительного просмотра.
* *optional* **int** `thumb_height`. Высота изображения предварительного просмотра.


### Формат ответа

Объект.

- **str** `uid`. Уникальный идентификатор изображения.
- **int** `length`. Размер в байтах.
- **str** `mime`. MIME-тип.
- **str** `name`. Имя.
- **str** `description`. Описание.
- **int** `width`. Ширина в пикселях.
- **int** `height`. Высота в пикселях.
- **object** `exif`. EXIF-данные.
- **str** `url`. URL загруженного файла.
- **str** `thumb_url`. URL изображения предварительного просмотра.


### Примеры

Запрос:

```
curl -v -X GET \
-d access_token=b81de38b9b9589f9a0ec569416e75a25 \
-d uid=5775fa3b523af5338fe839f3 \
http://test.com/api/1/pytsite.image/file
```

Ответ:

```
{
    "uid": "5775fa3b523af5338fe839f3",
    "length": 358362,
    "mime": "image/jpeg",
    "name": "HelloWorld.jpg",
    "description": "Uploaded via HTTP API",
    "width": 1024,
    "height": 768,
    "exif": {},
    "url": "http://test.com/image/resize/0/0/3c/ae/6ebfbdfb3dca5996.jpg",
    "thumb_url": "http://test.com/image/resize/450/450/3c/ae/6ebfbdfb3dca5996.jpg"
}
```
