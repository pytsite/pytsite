# pytsite.auth_driver_google

## Описание
Драйвер аутентификации [Google Sign In](https://developers.google.com/identity/sign-in/web/).

## Включение
В параметр конфигурации `app.autoload` добавить значение `pytsite.auth_driver_google`.

## Конфигурация
* Required `auth.google.client_id: <str>`. ID клиента Google. 
  См. https://developers.google.com/identity/sign-in/web/devconsole-project

## HTTP API
* См. [PytSite Authentication HTTP API](../../../auth/doc/ru/http_api.md).
* При отправке запросов к любой точке обязательна передача аргумента `driver` со значением 'google'.
* При отправке запросов к точке `sign_in` обязательна передача аргумента `id_token`, возвращаемого Google после 
  успешной аутентификации учётной записи пользователя. 

## Ссылки
* [Google Sign-In for Websites](https://developers.google.com/identity/sign-in/web/)
* [PytSite Authentication HTTP API](../../../auth/doc/ru/http_api.md)
