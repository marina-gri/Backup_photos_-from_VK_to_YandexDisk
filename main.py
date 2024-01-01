import json
from urllib.parse import urlencode
import requests
from tqdm import trange
import datetime
import time

class API_VK_get_photos:

    API_BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, owner_id, access_token):
        self.owner_id = owner_id
        self.access_token = access_token
        self.photo_info_dict = {}

    def get_photos_list(self):
        params_dict = {
            'access_token': self.access_token,
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': '5',
            'rev': '1',
            'v': '5.199'
        }
        response = requests.get(f'{self.API_BASE_URL}/photos.get?{urlencode(params_dict)}')
        return response.json()

    def get_photo_info_dict(self):
        best_size_url_list = []
        photo_name_list = []
        response_json = self.get_photos_list()
        json_list = []

        for item in response_json.get('response', {}).get('items'):
            best_size_url_list.append(item.get('sizes')[-1]['url'])

            if str(item.get('likes', {}).get('count')) in photo_name_list:
                photo_name = f"{str(item.get('likes', {}).get('count'))} {date_converter(item.get('date'))}"
            else:
                photo_name = str(item.get('likes', {}).get('count'))

            photo_name_list.append(photo_name)
            json_list.append({'file name': photo_name, 'photo size': item.get('sizes')[-1]['type']})

        with open('info.json', 'w', encoding='utf-8') as file:
            json.dump(json_list, file, indent=4)

        self.photo_info_dict['photo_url'] = best_size_url_list
        self.photo_info_dict['likes'] = photo_name_list
        return self.photo_info_dict

class API_Yandex_disk_send_photo:

    def __init__(self):
        self.base_yandex_api_url = 'https://cloud-api.yandex.net'
        self.base_params = {
            'Authorization': Yandex_Token
        }

    def create_folder(self, folder_name):
        url = f'{self.base_yandex_api_url}/v1/disk/resources'
        create_folder_params = {
            'path': folder_name
        }
        response = requests.put(url, params=create_folder_params, headers=self.base_params)
        return response.status_code

    def upload_photos(self):
        photo_info_dict = API_VK_get_photos(vk_id_user, VK_Token).get_photo_info_dict()
        self.create_folder(folder_name)
        print("Выполняется загрузка фото")
        for i in trange(len(photo_info_dict['photo_url'])):
            params = {
                'url': photo_info_dict['photo_url'][i],
                'path': f'{folder_name}/{photo_info_dict["likes"][i]}.jpeg'
            }
            response = requests.post(f'{self.base_yandex_api_url}/v1/disk/resources/upload', params=params, headers=self.base_params)
            time.sleep(1)
        print('Загрузка завершена')
        return response.status_code


with open('keys.json', 'r', encoding='utf-8') as file:
    keys = json.load(file)
    Yandex_Token = keys['Yandex_Token']
    VK_Token = keys['VK_Token']

def date_converter(date):
    time_stamp = datetime.datetime.fromtimestamp(date)
    str_date = time_stamp.strftime('%d-%m-%Y')
    return str_date


if __name__ == '__main__':
    vk_id_user = input('Введите id пользователя: ')
    folder_name = input('Введите название для папки: ')

    API_Yandex_disk_send_photo().upload_photos()





