# home work 23.01.2023 - http requests
from pprint import pprint
import requests
from datetime import datetime, timedelta

# функция для решения задачи №1
def get_most_clever_hero():
    url = "https://akabab.github.io/superhero-api/api"
    response = requests.get(url + '/all.json')
    all_dict = response.json()
    names = ['Hulk', 'Captain America', 'Thanos']
    result ={}
    for el in all_dict:
        if el['name'] in names:
            result[el['name']] = el['powerstats']['intelligence']
    most_clever = max(result.items(), key=lambda x: x[1])
    print(f'Самый умный супергерой: {most_clever[0]}\nего показатель: {most_clever[1]}')

# функция для решения задачи №3
def get_newest_questions():
    template = '%d.%m.%Y'
    today = datetime.now()
    daybeforeyesterday = today - timedelta(days=2)
    today_ = round(today.timestamp())
    daybeforeyesterday_ = round(daybeforeyesterday.timestamp())
    url = 'https://api.stackexchange.com//2.3/questions'
    params = {'fromdate': daybeforeyesterday_, 'todate': today_, 'order': 'desc',
              'sort': 'activity', 'site': 'stackoverflow', 'tagged': 'python'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.status_code == 200:
        print(f'{"-" * 90}\nСписок вопросов на сайте stackoverflow за период'
              f' c {daybeforeyesterday.strftime(template)} по {today.strftime(template)}'
              f' по теме Python\n{"-" * 90}')
        dct = response.json()
        for el in dct['items']:
            print(el['title'])


# класс для решения задачи №2
TOKEN = ''
class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        ''' получение списка всех файлов с яндекс.диска по заданному токену'''
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        dct = response.json()
        for el in dct['items']:
            print(el['name'].ljust(50), str(el['size']).ljust(15), el['created'][:10])
        return dct

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        # сначала получаем ссылку на место размещения файла (это для яндекса, другие могут отличаться)
        result = self._get_upload_link(disk_file_path=disk_file_path)
        url = result.get('href')
        # отправляем файл
        response = requests.put(url, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл успешно отправлен в хранилище Яндекс.Диск')

    def upload_test_file(self):
        self.upload_file_to_disk(disk_file_path='test_yandex_disk.txt', filename='test_yandex_disk.txt')


def react_on_kbd_command():
    com_dict = {
        '1': get_most_clever_hero,
        '2': ya.upload_test_file,
        '3': ya.get_files_list,
        '4': get_newest_questions
        }
    command = 'x'
    while command != '0':
        print('*' * 50)
        print('0 - выход из программы\n1 - определение самого умного супергероя\n'
              '2 - запись файла на Яндекс.Диск\n3 - список файлов на Яндекс.Диске\n'
              '4 - последние запросы по Python на stackoverflow\n'
              'Введите команду: ')
        command = input()
        try:
            if command != '0':
                com_dict[command]()
        except:
            print('Незнакомая команда')
    print('До свидания!')







if __name__ == '__main__':
    ya = YandexDisk(token=TOKEN)
    #ya.upload_file_to_disk(disk_file_path='test_yandex_disk.txt', filename='test_yandex_disk.txt'),
    #ya.get_files_list()
    #pprint(ya.get_files_list())
    react_on_kbd_command()


