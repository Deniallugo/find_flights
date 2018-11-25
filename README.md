# Поиск путей перелетов

## Установка
Необходимая версия python - 3.6
Все необходимые зависимости находятся в `requirements.txt`
для установки запустите:

`pip install -r requirements.txt`

## Запуск

`python3 main.py`

## Эндпоинты

`/all-paths/{source}/{destination}` - поиск  всех путей от исходной точки до заданной

`/best-path/{source}/{destination}?find_type={}&direction={}` - поиск  наилучшего пути. 

Параметры:

`find_type` - позволяет указать по какому параметру ищем лучшее предожение, по умолчанию `best`, т.е. лучшее по совокупности параметров.
 принимает значения `price`, `time`, `best`  

`direction` - позволяет указать направление для поиска уменьшение или увеличение. принимает занчения `desc` и `asc` 