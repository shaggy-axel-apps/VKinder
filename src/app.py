from db.models import engine, Session
from db.queries import (
    write_msg, add_user, add_user_photos, add_to_black_list,
    check_db_user, check_db_master,
)
from services.vk_functions import search_users, get_photo
from services.utils import sort_likes, json_create
from services.message_handler import (
    loop_bot, menu_bot, reg_new_user,
    show_info, go_to_blacklist, go_to_favorites
)
from settings import MIN_AGE, MAX_AGE


# Для работы с БД
session = Session()
connection = engine.connect()


if __name__ == '__main__':
    while True:
        msg_text, user_id = loop_bot()
        if msg_text.lower() == "vkinder":
            menu_bot(user_id)
            msg_text, user_id = loop_bot()

            # Регистрируем пользователя в БД
            if msg_text.lower() == 'да':
                reg_new_user(user_id)

            # Ищем партнера
            elif len(msg_text) > 1:
                sex = 0
                if msg_text.split()[0].lower() == 'девушка':
                    sex = 1
                elif msg_text.split()[0].lower() == 'мужчина':
                    sex = 2

                age = msg_text.split()[1]
                age_at = age.split('-')[0]
                if int(age_at) < MIN_AGE:
                    write_msg(user_id, f'Минимальный возраст - {MIN_AGE} лет.')
                    age_at = MIN_AGE
                age_to = age.split('-')[1]
                if int(age_to) > MAX_AGE:
                    write_msg(user_id, f'Максимальный возраст - {MAX_AGE} лет.')
                    age_to = MAX_AGE

                city = msg_text.split()[2].lower()
                # Ищем анкеты
                result = search_users(sex, int(age_at), int(age_to), city)
                json_create(result)
                current_user_id = check_db_master(user_id)
                # Производим отбор анкет
                for i in range(len(result)):
                    dating_user, blocked_user = check_db_user(result[i][3])
                    # Получаем фото и сортируем по лайкам
                    user_photo = get_photo(result[i][3])
                    if user_photo == 'нет доступа к фото' or dating_user is not None or blocked_user is not None:
                        continue
                    sorted_user_photo = sort_likes(user_photo)
                    # Выводим отсортированные данные по анкетам
                    write_msg(user_id, f'\n{result[i][0]}  {result[i][1]}  {result[i][2]}', )
                    try:
                        write_msg(user_id, f'фото:',
                                  attachment=','.join
                                  ([sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                                    sorted_user_photo[-3][1]]))
                    except IndexError:
                        for photo in range(len(sorted_user_photo)):
                            write_msg(user_id, f'фото:',
                                      attachment=sorted_user_photo[photo][1])
                    # Ждем пользовательский ввод
                    write_msg(user_id, '1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска')
                    msg_text, user_id = loop_bot()
                    if msg_text == '0':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info(user_id)
                    # Добавляем пользователя в избранное
                    elif msg_text == '1':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info(user_id)
                            break
                        # Пробуем добавить анкету в БД
                        try:
                            add_user(user_id, result[i][3], result[i][1],
                                     result[i][0], city, result[i][2], current_user_id.id)
                            # Пробуем добавить фото анкеты в БД
                            add_user_photos(user_id, sorted_user_photo[0][1],
                                            sorted_user_photo[0][0], current_user_id.id)
                        except AttributeError:
                            write_msg(user_id, 'Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота')
                            break
                    # Добавляем пользователя в черный список
                    elif msg_text == '2':
                        # Проверка на последнюю запись
                        if i >= len(result) - 1:
                            show_info(user_id)
                        # Блокируем
                        add_to_black_list(user_id, result[i][3], result[i][1],
                                          result[i][0], city, result[i][2],
                                          sorted_user_photo[0][1],
                                          sorted_user_photo[0][0], current_user_id.id)
                    elif msg_text.lower() == 'q':
                        write_msg(user_id, 'Введите Vkinder для активации бота')
                        break

            # Переходим в избранное
            elif msg_text == '2':
                go_to_favorites(user_id)

            # Переходим в черный список
            elif msg_text == '0':
                go_to_blacklist(user_id)
