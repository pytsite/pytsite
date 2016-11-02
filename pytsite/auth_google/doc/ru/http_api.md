# PytSite Google Authentication Driver

- См. [PytSite Authentication HTTP API](../../../auth/doc/ru/http_api.md).
- При отправке запросов к `auth/*` обязательна передача аргумента `driver` со значением 'google'.
- При отправке запросов к `POST auth/sign_in` обязательна передача аргумента `id_token`, возвращаемого Google после 
  успешной аутентификации учётной записи пользователя. 
