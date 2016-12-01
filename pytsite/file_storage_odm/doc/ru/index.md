# PytSite ODM File Storage

## Параметры конфигурации

- **int** `file_storage_odm.image_resize_limit_width`. Максимальная ширина изображения в пикселях при изменении 
  размеров. По умолчанию: 1200.
- **int** `file_storage_odm.image_resize_limit_height`. Максимальная высота изображения в пикселях при изменении 
  размеров. По умолчанию: 1200.
- **int** `file_storage_odm.image_resize_step`. Шаг ширины и высоты в пикселях при изменении размеров. По умолчанию: 50. 
  Смысл этого параметра в том, чтобы снизить нагрузку на сервер за счёт ограничения количества возможных размеров 
  стороны изображения при выполнении операций изменения размеров. Например, при попытке изменения изображения до 
  123х456 точек, каждая сторона будет выровнена до достижения кратности этому параметру: 150х500. Если бы значение 
  параметра было, например, 25, то стороны были бы выровнены до 125х475.  


## Router Endpoints

### /image/resize/[width]/[height]/[p1]/[p2]/[filename]

Получение изображения с сервера.

- **int** `width`. Ширина. Если 0, то будет использоваться ширина оригинального изображения.
- **int** `height`. Высота.  Если 0, то будет использоваться высота оригинального изображения.
- **str** `p1`. Подкаталог 1.
- **str** `p2`. Подкаталог 2.
- **str** `filename`. Имя файла.


Пример:

```
curl -v http://test.com/image/resize/450/450/57/e1/57e1a2823e7d890ed4fea374.png
```