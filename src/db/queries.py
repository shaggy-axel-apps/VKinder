from random import randrange

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from vkinder.settings import GROUP_TOKEN
from db.models import Session, BlackList, DatingUser, User, Photos


vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)

session = Session()


def delete_db_blacklist(ids: int) -> None:
    """ Удаляет пользователя из черного списка """
    current_user = session.query(BlackList).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


def delete_db_favorites(ids: int) -> None:
    """ Удаляет пользователя из избранного """
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


def check_db_master(ids: int) -> int:
    """ проверят зареган ли пользователь бота в БД """
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


def check_db_user(ids: int) -> tuple[DatingUser, BlackList]:
    """ проверят есть ли юзер в бд """
    dating_user = session.query(DatingUser).filter_by(
        vk_id=ids).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=ids).first()
    return dating_user, blocked_user


def check_db_black(ids: int):
    """ Проверят есть ли юзер в черном списке """
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    all_users = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
    return all_users


def check_db_favorites(ids: int) -> list[DatingUser]:
    """ Проверяет есть ли юзер в избранном """
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    return session.query(DatingUser).filter_by(id_user=current_users_id.id).all()


def write_msg(user_id: int, message: str, attachment=None) -> None:
    """ Пишет сообщение пользователю """
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})


def register_user(vk_id: int) -> bool:
    """ Регистрация пользователя """
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
    except (IntegrityError, InvalidRequestError):
        return False
    return True


def add_user(
    event_id: int, vk_id: int, first_name: str,
    last_name: str, city: str, link: str, id_user: int
) -> bool:
    """ Сохранение выбранного пользователя в БД """
    try:
        new_user = DatingUser(
            vk_id=vk_id,
            first_name=first_name, last_name=last_name,
            city=city, link=link, id_user=id_user
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


def add_user_photos(
    event_id: int, link_photo: str,
    count_likes: int, id_dating_user: int
) -> bool:
    """ Сохранение в БД фото добавленного пользователя """
    try:
        new_user = Photos(
            link_photo=link_photo,
            count_likes=count_likes,
            id_dating_user=id_dating_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'Фото пользователя сохранено в избранном')
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Фото уже сохранено)')
        return False
    return True


def add_to_black_list(
    event_id: int, vk_id: int, first_name: str,
    last_name: str, city: str, link: str,
    link_photo: str, count_likes: int, id_user: int
) -> bool:
    """ Добавление пользователя в черный список """
    try:
        new_user = BlackList(
            vk_id=vk_id,
            first_name=first_name, last_name=last_name,
            city=city, link=link, link_photo=link_photo,
            count_likes=count_likes, id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'Пользователь успешно заблокирован.')
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Пользователь уже в черном списке.')
        return False
    return True
