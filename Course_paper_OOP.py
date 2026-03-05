import logging
import requests
import sys
import json
from urllib.parse import quote
from setting import yd_token


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    breed = input('Введите текст на картинке с кошкой (на англ. языке): ').title()
    url = f'https://cataas.com/cat/says/{quote(breed)}'

    logging.info("Начинаем загрузку")

    response = requests.get(url, timeout=(5, 30))
    file_size = len(response.content)
    if response.status_code != 200:
        print('Что-то пошло не так')
        sys.exit(0)
    filename = f'{breed}.jpeg'

    logging.info("Картинка загружена")

    yd_base = 'https://cloud-api.yandex.net'
    params = {
        'path': 'PY-146'
    }
    headers = {
        'Authorization': f'OAuth {yd_token}'
    }

    logging.info("Создание папки PY-146 на Я.Диске")

    response = requests.put(f'{yd_base}/v1/disk/resources',
                            headers=headers,
                            params=params)

    if response.status_code not in (201, 409):
        print('Не удалось создать папку на Я.Диске: ')
        sys.exit(1)

    logging.info("Папка PY-146 готова к работе")

    logging.info("Идет загрузка картинки в папку")

    response = requests.post(f'{yd_base}/v1/disk/resources/upload',
                             headers=headers,
                             params={
                                'path': f'PY-146/{filename}',
                                'url': url
                                })

    if response.status_code not in (201, 202):
        print('Ошибка загрузки на Я.Диск: ')
        sys.exit(1)

    logging.info("Процесс завершен")

    info = {
        'filename': filename,
        'path': f'PY-146/{filename}',
        'byte': file_size
    }

    json_path = f'{breed}.json'

    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(info, jf, ensure_ascii=False, indent=4)

    return f'Создан файл: {json_path}'


print(main())
