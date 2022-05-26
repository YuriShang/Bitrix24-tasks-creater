from fast_bitrix24 import Bitrix


webhook = 'https://b24-ddwojh.bitrix24.ru/rest/1/qo5s8qed3wmy7gx6/'
b = Bitrix(webhook)

add_task = b.call('tasks.task.add', {
   "taskId":"1",
   "fields": {
       "TITLE": "Тестовая задача",
       "DESCRIPTION": "Тестовое описание",
       "PRIORITY": 2,
       "RESPONSIBLE_ID": 1,
   }
})
