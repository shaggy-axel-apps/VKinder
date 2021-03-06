from services.vk_functions import write_msg
from vkinder.settings import (
    MALE, FEMALE, MIN_AGE, MAX_AGE
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
