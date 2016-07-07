# PytSite Google Authentication Driver

- См. [PytSite Authentication HTTP API](../../../auth/doc/ru/http_api.md).
- При отправке запросов к любой точке обязательна передача аргумента `driver` со значением 'google'.
- При отправке запросов к точке `sign_in` обязательна передача аргумента `id_token`, возвращаемого Google после 
  успешной аутентификации учётной записи пользователя. 
