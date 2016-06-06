# PytSite Auth ODM API

## Модель Role
### Поля
* `name` `pytsite.odm.field.String`
* `description` `pytsite.odm.field.String`
* `permissions` `pytsite.odm.field.UniqueStringList`

## Модель User
### Поля
* `login` `pytsite.odm.field.String`
* `email` `pytsite.odm.field.String`
* `password` `pytsite.odm.field.String`
* `access_token` `pytsite.odm.field.String`
* `sign_in_count` `pytsite.odm.field.Integer`
* `last_sign_in` `pytsite.odm.field.DateTime`
* `last_activity` `pytsite.odm.field.DateTime`
* `status` `pytsite.odm.field.String`
* `roles` `pytsite.odm.field.RefsUniqueList`
* `follows` `pytsite.odm.field.RefsUniqueList`
* `is_online` `pytsite.odm.field.Virtual`
* `last_ip` `pytsite.odm.field.String`
* `geo_ip` `pytsite.odm.field.Virtual`
* `followers` `pytsite.odm.field.RefsUniqueList`
* `nickname` `pytsite.odm.field.String`
* `picture` `pytsite.odm.field.Ref`
* `picture_url` `pytsite.odm.field.Virtual`
* `first_name` `pytsite.odm.field.String`
* `last_name` `pytsite.odm.field.String`
* `full_name` `pytsite.odm.field.Virtual`
* `description` `pytsite.odm.field.String`
* `birth_date` `pytsite.odm.field.DateTime`
* `gender` `pytsite.odm.field.Integer`
* `phone` `pytsite.odm.field.String`
* `country` `pytsite.odm.field.String`
* `city` `pytsite.odm.field.String`
* `urls` `pytsite.odm.field.StringList`
* `options` `pytsite.odm.field.Dict`
