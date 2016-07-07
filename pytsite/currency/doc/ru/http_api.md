# PytSite Currency HTTP API

## GET pytsite.currency/list

Получение списка валют.


### Аргументы

- *required* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).


### Формат ответа

Объект.

- **str** `CODE`. Трёхсимвольный код валюты по [ISO 4217](https://ru.wikipedia.org/wiki/ISO_4217).
    - **str** `title`. Название.
    - **str** `symbol`. Символ.


### Примеры

Запрос:

```
curl -X GET \
-d access_token='755fade9c84061c663714ee86d586cb4' \
http://test.com/api/1/pytsite.currency/list
```

Ответ:

```
{
    "UAH":
    {
        "title": "Украинская гривна",
        "symbol": "₴"
    },
    "USD":
    {
        "title": "Доллар США",
        "symbol": "$"
    }
}
```
