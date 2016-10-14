# PytSite File HTTP API

Перед изучением этого документа убедитесь, что разобрались с [PytSite HTTP API](../../../http_api/doc/ru/index.md).


## POST file/upload

Загрузка файлов. Для работы с этим методом **должен** использоваться 
[HTTP Multipart Content-Type](https://www.ietf.org/rfc/rfc2388.txt)


### Аргументы

- *required* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *required* **binary** `file{N}`. Загружаемый файл, где `{N}` -- порядковый номер файла.  


### Формат ответа

Массив объектов.

- **str** `uid`. Уникальный идентификатор файла.


### Примеры

Запрос:

```
curl \
-F access_token=b81de38b9b9589f9a0ec569416e75a25 \
-F file1=@/home/user/HelloWorld.jpg \
-F file2=@/home/user/HereWeGo.png \
http://test.com/api/1/file/upload
```

Ответ:

```
[
    {"uid": "file_image:57fcda463e7d89205a0c8d8f"},
    {"uid": "file_image:57fcda583e7d89205a0c8d90"}
]
```


## GET file/info

Получение информации о файле.


### Аргументы

* *required* **str** `uid`. Уникальный идентификатор файла.  
* *optional* **int** `thumb_width`. Ширина изображения предварительного просмотра.
* *optional* **int** `thumb_height`. Высота изображения предварительного просмотра.

Аргументы `thumb_width` и `thumb_height` должны иметь значение в пределах от 0 до значений, определённых в [параметрах 
конфигурации](reg.md) `file.resize_limit_width` и `file.resize_limit_height` соответственно. В случае превышения 
значения будут автоматически скорректированы до максимально-возможных.


### Формат ответа

Объект.

Поля для всех файлов.

- **str** `uid`. Уникальный идентификатор файла.
- **int** `length`. Размер файла в байтах.
- **str** `mime`. MIME-тип.
- **str** `url`. URL файла.
- **str** `thumb_url`. URL предварительного просмотра.


Дополнительные поля для файлов изображений.

- **int** `width`. Ширина изображения в пикселях.
- **int** `height`. Высота изображения в пикселях.

### Примеры

Запрос:

```
curl -X GET \
-d uid=file_image:57fcda463e7d89205a0c8d8f \
-d thumb_width=800 \
-d thumb_height=600 \
http://test.com/api/1/file/info
```

Ответ:

```
{
    "uid": "file_image:57fcda463e7d89205a0c8d8f",
    "length": 358362,
    "mime": "image/jpeg",
    "url": "http://test.com/image/resize/0/0/57/fc/57fcda463e7d89205a0c8d8f.jpg",
    "thumb_url": "http://test.com/image/resize/800/600/57/fc/57fcda463e7d89205a0c8d8f.jpg",
    "width": 1024,
    "height": 768
}
```
