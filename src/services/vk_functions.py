from random import randrange
from typing import Optional

from vk_api import VkApi
from vk_api.exceptions import ApiError
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll
from vk_api.vk_api import VkApiGroup

from db.tuple_models import Person, Photo
from db.models import engine, Session
from vkinder.settings import GROUP_TOKEN, USER_TOKEN, V


# Для работы с ВК
vk = VkApiGroup(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)

# Для работы с БД
session = Session()
connection = engine.connect()


def search_users_api(sex: int, age_at: int, age_to: int, city: str) -> list[Person]:
    """ Ищет людей по критериям """
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk_ = VkApi(token=USER_TOKEN)
    response = vk_.method(
        'users.search',
        {
            'sort': 1, 'status': 1, 'has_photo': 1, 'count': 25, 'online': 1,
            'sex': sex, 'age_from': age_at, 'age_to': age_to, 'hometown': city
        })
    for field in response['items']:
        print(field)
        all_persons.append(Person(
            vk_id=field["id"],
            first_name=field["first_name"],
            last_name=field["last_name"],
            link=f"{link_profile}{field['id']}",
            can_access_closed=field['can_access_closed'],
            is_closed=field["is_closed"],
        ))
    return all_persons


def get_photo(user_owner_id: int) -> Optional[list[Photo]]:
    """ Находит фото людей """
    vk_ = VkApi(token=USER_TOKEN)
    try:
        response = vk_.method(
            'photos.get',
            {'access_token': USER_TOKEN, 'v': V, 'owner_id': user_owner_id,
             'album_id': 'profile', 'count': 10, 'extended': 1, 'photo_sizes': 1}
        )
    except ApiError:
        return
    users_photos = []
    for item in response["items"]:
        try:
            popular = item['likes']['count'] + item['comments']['count']
            users_photos.append(Photo(
                popular=popular,
                owner_id=item["owner_id"],
                photo=f"photo{item['owner_id']}_{item['id']}"
            ))
        except IndexError:
            users_photos.append(
                Photo(popular=0, owner_id=item["owner_id"], photo=None))
    return users_photos


def write_msg(user_id: int, message: str, keyboard: VkKeyboard = None, attachment=None) -> None:
    """ Пишет сообщение пользователю """
    my_keyboard = keyboard
    if keyboard:
        my_keyboard = keyboard.get_keyboard()
    vk.method(
        'messages.send',
        {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attachment,
            'keyboard': my_keyboard
        }
    )
