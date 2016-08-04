# PytSite Flag HTTP API

Перед изучением этого документа убедитесь, что разобрались с [PytSite HTTP API](../../../http_api/doc/ru/index.md).


## PATCH pytsite.flag/toggle

Установка/снятие флага для сущности. 


### Аргументы
- *required* **str** `access_token`. [Токен доступа](../../../auth/doc/ru/http_api.md#post-pytsiteauthsign_in).
- *required* **str** `model`. Модель сущности.
- *required* **str** `uid`. UID сущности.


### Формат ответа

Объект.

- **bool** `status`. Состояние флага для данного пользователя. true -- установлен, false -- снят.
- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

Запрос:

```
curl -X PATCH \
-d access_token=77aaea01a5e58ac3a7d114f418231fa6 \
-d model=product \
-d uid=57a304e2523af552d17a4dfb \
http://test.com/api/1/pytsite.flag/toggle
```


Ответ:
```
{
    "status": true,
    "count": 728
}
```
