from services.message_handler import (
    menu_bot, go_to_blacklist,
    go_to_favorites, does_not_exists,
    search_users
)


COMMANDS = {
    "/help": menu_bot,
    "/favorites": go_to_favorites,
    "/blacklist": go_to_blacklist,

    "does_not_exists": does_not_exists,
}

def get_commands():
    return COMMANDS
