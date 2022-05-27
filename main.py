from fast_bitrix24 import Bitrix
from datetime import date, timedelta
import requests 


def main():
    # сегодняшний день + 3 дня
    day = ''.join(str(date.today() + timedelta(days=3)).split('-')) 
    webhook = 'здесь должен быть ваш вебхук'

    # создаем экземпляр класса Bitrix и передаем в него свой вебхук
    my_bitrix = Bitrix(webhook)

    # с помощью гет запроса проверяем является ли переданный день праздничным:
    request =requests.get(f'https://isdayoff.ru/{day}?holiday=1') 

    # если ответ == '8', то день праздничный. Инфа с оф. телеграма сервиса, работает только для России.
    # если условие выполняется, создаем задачку в б24
    if request.text == '8':
        my_bitrix.call('tasks.task.add', {
            "taskId":"1",
            "fields": {
                "TITLE": "Тестовая задача",
                "DESCRIPTION": "Тестовое описание",
                "PRIORITY": 2,
                "RESPONSIBLE_ID": 1,
            }
        })


if __name__ == "__main__":
    main()