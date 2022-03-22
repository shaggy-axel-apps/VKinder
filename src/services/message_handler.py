from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from settings import GROUP_TOKEN
from db.queries import (
    write_msg, register_user, check_db_black, check_db_favorites,
    delete_db_blacklist, delete_db_favorites)


vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)


def loop_bot() -> tuple[str, int]:
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


def menu_bot(id_num):
    write_msg(id_num,
              f"Вас приветствует бот - Vkinder\n"
              f"\nЕсли вы используете его первый раз - пройдите регистрацию.\n"
              f"Для регистрации введите - Да.\n"
              f"Если вы уже зарегистрированы - начинайте поиск.\n"
              f"\nДля поиска - девушка 18-25 Москва\n"
              f"Перейти в избранное нажмите - 2\n"
              f"Перейти в черный список - 0\n")


def show_info(user_id):
    write_msg(user_id, f'Это была последняя анкета.'
                       f'Перейти в избранное - 2'
                       f'Перейти в черный список - 0'
                       f'Поиск - девушка 18-35 белгород'
                       f'Меню бота - Vkinder')


def reg_new_user(id_num):
    write_msg(id_num, 'Вы прошли регистрацию.')
    write_msg(id_num,
              f"Vkinder - для активации бота\n")
    register_user(id_num)


def go_to_favorites(ids):
    alls_users = check_db_favorites(ids)
    write_msg(ids, f'Избранные анкеты:')
    for nums, users in enumerate(alls_users):
        write_msg(ids, f'{users.first_name}, {users.last_name}, {users.link}')
        write_msg(ids, '1 - Удалить из избранного, 0 - Далее \nq - Выход')
        msg_texts, user_ids = loop_bot()
        if msg_texts == '0':
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f'Это была последняя анкета.\n'
                                    f'Vkinder - вернуться в меню\n')
        # Удаляем запись из бд - избранное
        elif msg_texts == '1':
            delete_db_favorites(users.vk_id)
            write_msg(user_ids, f'Анкета успешно удалена.')
            if nums >= len(alls_users) - 1:
                write_msg(user_ids, f'Это была последняя анкета.\n'
                                    f'Vkinder - вернуться в меню\n')
        elif msg_texts.lower() == 'q':
            write_msg(ids, 'Vkinder - для активации бота.')
            break


def go_to_blacklist(ids):
    all_users = check_db_black(ids)
    write_msg(ids, f'Анкеты в черном списке:')
    for num, user in enumerate(all_users):
        write_msg(ids, f'{user.first_name}, {user.last_name}, {user.link}')
        write_msg(ids, '1 - Удалить из черного списка, 0 - Далее \nq - Выход')
        msg_texts, user_ids = loop_bot()
        if msg_texts == '0':
            if num >= len(all_users) - 1:
                write_msg(user_ids, f'Это была последняя анкета.\n'
                                    f'Vkinder - вернуться в меню\n')
        # Удаляем запись из бд - черный список
        elif msg_texts == '1':
            print(user.id)
            delete_db_blacklist(user.vk_id)
            write_msg(user_ids, f'Анкета успешно удалена')
            if num >= len(all_users) - 1:
                write_msg(user_ids, f'Это была последняя анкета.\n'
                                    f'Vkinder - вернуться в меню\n')
        elif msg_texts.lower() == 'q':
            write_msg(ids, 'Vkinder - для активации бота.')
            break
