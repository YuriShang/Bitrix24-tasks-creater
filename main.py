from fast_bitrix24 import Bitrix
from datetime import date, timedelta
import time
import requests

WEBHOOK = 'Ваш вебхук'


class TaskCreater:
    def __init__(self, webhook):
        # создаем экземпляр класса Bitrix и передаем в него свой вебхук
        self.my_bitrix = Bitrix(webhook)

        # список задач, которые мы откуда-то получили, и которые необходимо добавить в б24
        self.tasks = [{"taskId": "1",
                       "fields": {
                           "TITLE": "Тестовая задача 1",
                           "DESCRIPTION": "Тестовое описание 1",
                           "PRIORITY": 2,
                           "RESPONSIBLE_ID": 1,
                       }
                       },
                      {"taskId": "2",
                       "fields": {
                           "TITLE": "Тестовая задача 2",
                           "DESCRIPTION": "Тестовое описание 2",
                           "PRIORITY": 2,
                           "RESPONSIBLE_ID": 1,
                       }
                       },
                      {"taskId": "3",
                       "fields": {
                           "TITLE": "Тестовая задача 3",
                           "DESCRIPTION": "Тестовое описание 3",
                           "PRIORITY": 2,
                           "RESPONSIBLE_ID": 1,
                       }
                       }]

        # получаем имена задач
        self.tasks_names = [i.get("fields").get("TITLE") for i in self.tasks]

        # флаг, свидетельствующий о загрузке задач
        self.tasks_uploaded = True

    def time_checker(self):
        """
        Каждые пол часа проверяем не наступило ли 8 часов утра
        """
        while True:
            local_time = time.localtime()
            if local_time.tm_hour == 13 and self.tasks_uploaded:
                # Ежедневно запускаем функцию create_tasks
                self.tasks_uploaded = False
                self.create_tasks()
                # Загрузили задачи, ждем час
                time.sleep(3600)
            elif not self.tasks_uploaded:
                # Если по какой-то причине задачи не загрузились, пробуем заново каждые 30 мин
                self.create_tasks()
            time.sleep(1800)

    def create_tasks(self):
        """
        Функция запускается ежедневно и проверяет не является ли требуемый день, праздничным.
        Если да, то необходимые задачи загружаются в б24
        """

        # сегодняшний день + 3 дня
        day = ''.join(str(date.today() + timedelta(days=3)).split('-'))

        # с помощью гет запроса проверяем является ли переданный день праздничным:
        request = requests.get(f'https://isdayoff.ru/{day}?holiday=1')

        # Условие выполняется в двух случаях: праздничный день (ответ == '8') и наличие задач
        if request.text == '0' and self.tasks:
            for task in self.tasks:
                self.my_bitrix.call('tasks.task.add', task)

            # запрашиваем загруженные задачи, чтобы убедиться, что они успешно добавились
            get_tasks = self.my_bitrix.call('tasks.task.list',
                                            {"select": ['TITLE']})

            # Названия только что загруженных задач
            uploaded_tasks_names = [get_tasks[i].get('title') for i in range(-len(self.tasks_names), 0)]
            print(uploaded_tasks_names)

            if self.tasks_names == uploaded_tasks_names:
                print('tasks created')
                self.tasks_uploaded = True


if __name__ == "__main__":
    task_creater = TaskCreater(WEBHOOK)
    task_creater.time_checker()
