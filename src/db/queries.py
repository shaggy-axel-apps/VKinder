from random import randrange

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from settings import GROUP_TOKEN
from db.models import session, BlackList, DatingUser, User, Photos


vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)


# Удаляет пользователя из черного списка
def delete_db_blacklist(ids):
    current_user = session.query(BlackList).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


# Удаляет пользователя из избранного
def delete_db_favorites(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


# проверят зареган ли пользователь бота в БД
def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


# проверят есть ли юзер в бд
def check_db_user(ids):
    dating_user = session.query(DatingUser).filter_by(
        vk_id=ids).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=ids).first()
    return dating_user, blocked_user


# Проверят есть ли юзер в черном списке
def check_db_black(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    all_users = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
    return all_users


# Проверяет есть ли юзер в избранном
def check_db_favorites(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    alls_users = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
    return alls_users


# Пишет сообщение пользователю
def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})


# Регистрация пользователя
def register_user(vk_id):
    try:
        new_user = User(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


# Сохранение выбранного пользователя в БД
def add_user(event_id, vk_id, first_name, second_name, city, link, id_user):
    try:
        new_user = DatingUser(
            vk_id=vk_id,
            first_name=first_name,
            second_name=second_name,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в избранном.')
        return False


# Сохранение в БД фото добавленного пользователя
def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
    try:
        new_user = Photos(
            link_photo=link_photo,
            count_likes=count_likes,
            id_dating_user=id_dating_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Фото пользователя сохранено в избранном')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Невозможно добавить фото этого пользователя(Уже сохранено)')
        return False


# Добавление пользователя в черный список
def add_to_black_list(event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user):
    try:
        new_user = BlackList(
            vk_id=vk_id,
            first_name=first_name,
            second_name=second_name,
            city=city,
            link=link,
            link_photo=link_photo,
            count_likes=count_likes,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Пользователь успешно заблокирован.')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в черном списке.')
        return False
