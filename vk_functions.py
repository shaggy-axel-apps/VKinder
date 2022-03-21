import datetime
import json

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from vk_api.exceptions import ApiError

from vk_config import GROUP_TOKEN, USER_TOKEN, V
from models import engine, Session


# Для работы с ВК
vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()

""" 
ФУНКЦИИ ПОИСКА
"""


# Ищет людей по критериям
def search_users(sex, age_at, age_to, city):
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk_ = VkApi(token=USER_TOKEN)
    response = vk_.method('users.search',
                          {'sort': 1,
                           'sex': sex,
                           'status': 1,
                           'age_from': age_at,
                           'age_to': age_to,
                           'has_photo': 1,
                           'count': 25,
                           'online': 1,
                           'hometown': city
                           })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
    return all_persons
    # return True


# Находит фото людей
def get_photo(user_owner_id):
    vk_ = VkApi(token=USER_TOKEN)
    try:
        response = vk_.method('photos.get',
                              {
                                  'access_token': USER_TOKEN,
                                  'v': V,
                                  'owner_id': user_owner_id,
                                  'album_id': 'profile',
                                  'count': 10,
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
    except ApiError:
        return 'нет доступа к фото'
    users_photos = []
    for i in range(10):
        try:
            users_photos.append(
                [response['items'][i]['likes']['count'],
                 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
        except IndexError:
            users_photos.append(['нет фото.'])
    return users_photos
    # return True


""" 
ФУНКЦИИ СОРТИРОВКИ, ОТВЕТА, JSON
"""


# Сортируем фото по лайкам, удаляем лишние элементы
def sort_likes(photos):
    result = []
    for element in photos:
        if element != ['нет фото.'] and photos != 'нет доступа к фото':
            result.append(element)
    return sorted(result)


# JSON file create with result of programm
def json_create(lst):
    today = datetime.date.today()
    today_str = f'{today.day}.{today.month}.{today.year}'
    res = {}
    res_list = []
    for info in lst:
        res['data'] = today_str
        res['first_name'] = info[0]
        res['second_name'] = info[1]
        res['link'] = info[2]
        res['id'] = info[3]
        res_list.append(res.copy())

    with open("result.json", "a", encoding='UTF-8') as write_file:
        json.dump(res_list, write_file, ensure_ascii=False)

    print(f'Информация о загруженных файлах успешно записана в json файл.')



