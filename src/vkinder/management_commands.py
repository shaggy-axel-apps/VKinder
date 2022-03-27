from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from db.models import create_all
from db.queries import save_user
from vkinder.settings import (
    GROUP_TOKEN, BUTTONS, START_COMMAND, MIGRATE_COMMAND)
from services import COMMANDS
from services.parsers import parse_message


def loop_bot(**options) -> None:
    vk = VkApi(token=GROUP_TOKEN)
    longpoll = VkLongPoll(vk)

    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message: str = this_event.text

                if message.lower() == START_COMMAND:
                    save_user(this_event.user_id)
                    message = "/help"

                if message in BUTTONS:
                    message = f"/{message.lower().replace(' ', '')}"

                if message.startswith('/'):
                    try:
                        COMMANDS[message](this_event.user_id)
                    except KeyError:
                        COMMANDS["does_not_exists"](this_event.user_id)
                else:
                    parse_message(this_event.user_id, message)


def migrate(**options):
    create_all()


MANAGEMENT_COMMANDS = {
    START_COMMAND: loop_bot,
    MIGRATE_COMMAND: migrate,
}

def run(command: str, **options):
    MANAGEMENT_COMMANDS[command](**options)