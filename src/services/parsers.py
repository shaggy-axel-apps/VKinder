from services import COMMANDS, search_users
from services.vk_functions import write_msg
from db.queries import (
    delete_from_blacklist, delete_from_favorites,
    add_pair_to_blacklist, add_pair_to_favorites
)
from vkinder.settings import (
    START_SEARCH_WORDS, MALE, FEMALE, MIN_AGE, MAX_AGE
)


def get_sex_from_message(message: str) -> int:
    """ Get Sex from message for searching """
    if message.split()[0].lower() in FEMALE:
        return 1
    elif message.split()[0].lower() in MALE:
        return 2
    return 0


def get_age_from_message(vk_id, message: str) -> tuple[int, int]:
    """ Get Age from message for searching """
    age = message.split()[1]

    try:
        age_from = int(age.split('-')[0])
    except:
        age_from = MIN_AGE
        write_msg(vk_id, 'Возраст должен быть целым числом')

    if age_from < MIN_AGE:
        write_msg(vk_id, f'Минимальный возраст - {MIN_AGE} лет.')
        age_from = MIN_AGE

    try:
        age_to = int(age.split('-')[1])
    except:
        age_to = MAX_AGE
        write_msg(vk_id, 'Возраст должен быть целым числом')
    if age_to > MAX_AGE:
        write_msg(vk_id, f'Максимальный возраст - {MAX_AGE} лет.')
        age_to = MAX_AGE

    return age_from, age_to


def blacklist_parser(vk_id, message: str, add: bool):
    blacklist_vk_id = message.split()[-1]
    if add:
        add_pair_to_blacklist(vk_id=blacklist_vk_id, id_user=vk_id)
        write_msg(vk_id, f'Анкета пользователя {blacklist_vk_id} успешно добавлена')
    else:
        delete_from_blacklist(vk_id=blacklist_vk_id, id_user=vk_id)
        write_msg(vk_id, f'Анкета пользователя {blacklist_vk_id} успешно удалена')


def favorites_parser(vk_id, message: str, add: bool):
    favorites_vk_id = message.split()[-1]
    if add:
        add_pair_to_favorites(vk_id=favorites_vk_id, id_user=vk_id)
        write_msg(vk_id, f'Анкета пользователя {favorites_vk_id} успешно добавлена')
    else:
        delete_from_favorites(vk_id=favorites_vk_id, id_user=vk_id)
        write_msg(vk_id, f'Анкета пользователя {favorites_vk_id} успешно удалена')


def parse_message(vk_id: int, message: str):
    if message.lower().startswith("remove"):
        if "blacklist" in message.lower():
            blacklist_parser(vk_id, message, False)
        elif "favorites" in message.lower():
            favorites_parser(vk_id, message, False)

    elif message.lower().startswith("add"):
        if "blacklist" in message.lower():
            blacklist_parser(vk_id, message, True)
        elif "favorites" in message.lower():
            favorites_parser(vk_id, message, True)

    elif message.lower().startswith(START_SEARCH_WORDS):
        search_users(vk_id, message)

    else:
        COMMANDS["does_not_exists"](vk_id)
