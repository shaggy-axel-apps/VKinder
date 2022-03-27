from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from vkinder.settings import GROUP_TOKEN
from db.models import Session, BlackList, DatingUser, User

vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)

session = Session()


def save_user(vk_id: int) -> bool:
    """ Регистрация пользователя """
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
    except (IntegrityError, InvalidRequestError):
        return False
    return True


def delete_from_blacklist(vk_id: int) -> None:
    """ Удаляет пользователя из черного списка """
    current_user = session.query(BlackList).filter_by(vk_id=vk_id).first()
    session.delete(current_user)
    session.commit()


def delete_from_favorites(vk_id: int) -> None:
    """ Удаляет пользователя из избранного """
    current_user = session.query(DatingUser).filter_by(vk_id=vk_id).first()
    session.delete(current_user)
    session.commit()


def get_user(vk_id: int) -> User:
    """ получаем пользователя по `vk_id` """
    return session.query(User).filter_by(vk_id=vk_id).first()


def check_pair_already_exists(vk_id: int) -> bool:
    """ проверят есть ли юзер в бд """
    dating_user = session.query(DatingUser).filter_by(
        vk_id=vk_id).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=vk_id).first()
    return bool(dating_user) or bool(blocked_user)


def get_users_from_black_list(vk_id: int) -> list[BlackList]:
    """ Сбор пользователей из `черного списка` """
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(BlackList).filter_by(id_user=user.id).all()


def get_users_from_favorites(vk_id: int) -> list[DatingUser]:
    """ Сбор пользователей из `избранных` """
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(DatingUser).filter_by(id_user=user.id).all()


def add_pair_to_favorites(
    vk_id: int, id_user: int
) -> bool:
    """ Сохранение выбранного пользователя в БД """
    try:
        new_user = DatingUser(
            vk_id=vk_id, id_user=id_user
        )
        session.add(new_user)
        session.commit()
        return 'ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ'
    except (IntegrityError, InvalidRequestError):
        return 'Пользователь уже в избранном.'


def add_pair_to_blacklist(
    vk_id: int, id_user: int
) -> bool:
    """ Добавление пользователя в черный список """
    try:
        new_user = BlackList(
            vk_id=vk_id, id_user=id_user
        )
        session.add(new_user)
        session.commit()
        return 'Пользователь успешно заблокирован.'
    except (IntegrityError, InvalidRequestError):
        return 'Пользователь уже в черном списке.'
