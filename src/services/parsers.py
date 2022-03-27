from services import COMMANDS, search_users
from services.vk_functions import write_msg
from db.queries import (
    delete_from_blacklist, delete_from_favorites,
    add_pair_to_blacklist, add_pair_to_favorites, get_user
)
from vkinder.settings import START_SEARCH_WORDS


def blacklist_parser(vk_id, message: str, add: bool):
    blacklist_vk_id = int(message.split()[-1])
    current_user = get_user(vk_id)
    if add:
        message = add_pair_to_blacklist(vk_id=blacklist_vk_id, user_id=current_user.id)
        write_msg(vk_id, message)
    else:
        message = delete_from_blacklist(vk_id=blacklist_vk_id, user_id=current_user.id)
        write_msg(vk_id, message)


def favorites_parser(vk_id, message: str, add: bool):
    favorites_vk_id = int(message.split()[-1])
    current_user = get_user(vk_id)
    if add:
        message = add_pair_to_favorites(vk_id=favorites_vk_id, user_id=current_user.id)
        write_msg(vk_id, message)
    else:
        message = delete_from_favorites(vk_id=favorites_vk_id, user_id=current_user.id)
        write_msg(vk_id, message)


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
