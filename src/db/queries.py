from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from vkinder.settings import GROUP_TOKEN
from db.models import Session, BlackList, DatingUser, User

vk = VkApi(token=GROUP_TOKEN)
longpoll = VkLongPoll(vk)


def save_user(vk_id: int) -> bool:
    """ Регистрация пользователя """
    session = Session()
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
    except (IntegrityError, InvalidRequestError):
        return False
    return True


def delete_from_blacklist(vk_id: int, user_id: int) -> None:
    """ Удаляет пользователя из черного списка """
    session = Session()
    current_user = session.query(BlackList).filter_by(
        vk_id=vk_id, user_id=user_id).first()
    session.delete(current_user)
    session.commit()
    return f"Пользователь {vk_id} успешно удален из Черного Списка"


def delete_from_favorites(vk_id: int, user_id: int) -> None:
    """ Удаляет пользователя из избранного """
    session = Session()
    current_user = session.query(DatingUser).filter_by(
        vk_id=vk_id, user_id=user_id).first()
    session.delete(current_user)
    session.commit()
    return f"Пользователь {vk_id} успешно удален из Избранных"


def get_user(vk_id: int) -> User:
    """ получаем пользователя по `vk_id` """
    session = Session()
    return session.query(User).filter_by(vk_id=vk_id).first()


def check_pair_already_exists(vk_id: int) -> bool:
    """ проверят есть ли юзер в бд """
    session = Session()
    dating_user = session.query(DatingUser).filter_by(
        vk_id=vk_id).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=vk_id).first()
    return bool(dating_user) or bool(blocked_user)


def get_users_from_black_list(vk_id: int) -> list[BlackList]:
    """ Сбор пользователей из `черного списка` """
    session = Session()
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(BlackList).filter_by(user_id=user.id).all()


def get_users_from_favorites(vk_id: int) -> list[DatingUser]:
    """ Сбор пользователей из `избранных` """
    session = Session()
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(DatingUser).filter_by(user_id=user.id).all()


def add_pair_to_favorites(
    vk_id: int, user_id: int
) -> bool:
    """ Сохранение выбранного пользователя в БД """
    session = Session()
    try:
        new_user = DatingUser(
            vk_id=vk_id, user_id=user_id
        )
        session.add(new_user)
        session.commit()
        return f'Пользователь {vk_id} успешно добавлен в избранное'
    except (IntegrityError, InvalidRequestError) as e:
        return f'Пользователь {vk_id} уже в избранном.\n {e}'


def add_pair_to_blacklist(
    vk_id: int, user_id: int
) -> bool:
    """ Добавление пользователя в черный список """
    session = Session()
    try:
        new_user = BlackList(
            vk_id=vk_id, user_id=user_id
        )
        session.add(new_user)
        session.commit()
        return f'Пользователь {vk_id} успешно заблокирован.'
    except (IntegrityError, InvalidRequestError):
        return f'Пользователь {vk_id} уже в черном списке.'
