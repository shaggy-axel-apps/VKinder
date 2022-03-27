from db.queries import (
    get_users_from_black_list, get_users_from_favorites,
    check_pair_already_exists
)
from services.vk_functions import write_msg, get_photo, search_users_api
from services.keyboards import (
    get_menu_keyboard, get_remove_keyboard, get_user_rate_keyboard
)
from services.validators import get_sex_from_message, get_age_from_message
from services.utils import sort_photo


def menu_bot(vk_id: int) -> None:
    keyboard = get_menu_keyboard()
    message = ("Вас приветствует бот - Vkinder")
    write_msg(vk_id, message=message, keyboard=keyboard)


def search_users(vk_id: int, message: str) -> None:
    """ search required pair for user """
    try:
        sex = get_sex_from_message(message)
        age_from, age_to = get_age_from_message(vk_id, message)
        city = message.split()[2].capitalize()
    except IndexError:
        return write_msg(vk_id, "invalid searching parametrs, try again")

    result = search_users_api(sex, age_from, age_to, city)
    # Производим отбор анкет
    for user in result:
        if check_pair_already_exists(user.vk_id):
            continue

        # Получаем фото и сортируем по лайкам
        user_photos = get_photo(user.vk_id)
        if not user_photos:
            continue

        user_photos = sort_photo(user_photos)

        keyboard = get_user_rate_keyboard(user.vk_id)
        # Выводим отсортированные данные по анкетам
        write_msg(
            vk_id, f'{user.first_name} {user.last_name}\n{user.link}',
            attachment=','.join(
                [user_photo.photo
                 for counter, user_photo in enumerate(user_photos)
                 if counter < 3]
            ),
            keyboard=keyboard
        )


def go_to_favorites(vk_id: int) -> None:
    """ Send users from favorites list """
    all_users = get_users_from_favorites(vk_id)
    write_msg(vk_id, f'Избранные анкеты:')
    for user in all_users:
        keyboard = get_remove_keyboard("Favorites", user.vk_id)
        write_msg(vk_id, f'{user.vk_id}', keyboard=keyboard)
        # write_msg(vk_id, f'{user.first_name}, {user.last_name}, {user.link}', keyboard=keyboard)


def go_to_blacklist(vk_id: int) -> None:
    """ Send users from black list """
    all_users = get_users_from_black_list(vk_id)
    write_msg(vk_id, 'Анкеты в черном списке:')
    for user in all_users:
        keyboard = get_remove_keyboard("BlackList", user.vk_id)
        write_msg(vk_id, f'{user.vk_id}', keyboard=keyboard)
        # write_msg(vk_id, f'{user.first_name}, {user.last_name}, {user.link}', keyboard=keyboard)


def does_not_exists(vk_id: int) -> None:
    write_msg(vk_id, 'Команда не найдена')
