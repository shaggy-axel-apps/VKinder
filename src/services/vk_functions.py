from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from vk_api.exceptions import ApiError

from vkinder.settings import GROUP_TOKEN, USER_TOKEN, V
from db.models import engine, Session


# Для работы с ВК
vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)

# Для работы с БД
session = Session()
connection = engine.connect()


def search_users(sex, age_at, age_to, city):
    """ Ищет людей по критериям """
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk_ = VkApi(token=USER_TOKEN)
    response = vk_.method(
        'users.search',
        {'sort': 1,
         'sex': sex,
         'status': 1,
         'age_from': age_at,
         'age_to': age_to,
         'has_photo': 1,
         'count': 25,
         'online': 1,
         'hometown': city})
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
    return all_persons


def get_photo(user_owner_id):
    """ Находит фото людей """
    vk_ = VkApi(token=USER_TOKEN)
    try:
        response = vk_.method(
            'photos.get',
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
