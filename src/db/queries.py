from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from vkinder.settings import GROUP_TOKEN
from db.models import Session, BlackList, DatingUser, User, Photos

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


def check_registration(vk_id: int) -> int:
    """ проверят зареган ли пользователь бота в БД """
    return session.query(User).filter_by(vk_id=vk_id).first()


def check_pair_already_exists(vk_id: int) -> tuple[DatingUser, BlackList]:
    """ проверят есть ли юзер в бд """
    dating_user = session.query(DatingUser).filter_by(
        vk_id=vk_id).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=vk_id).first()
    return dating_user, blocked_user


def get_users_from_black_list(vk_id: int) -> list[BlackList]:
    """ Сбор пользователей из `черного списка` """
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(BlackList).filter_by(id_user=user.id).all()


def get_users_from_favorites(vk_id: int) -> list[DatingUser]:
    """ Сбор пользователей из `избранных` """
    user = session.query(User).filter_by(vk_id=vk_id).first()
    return session.query(DatingUser).filter_by(id_user=user.id).all()


def add_pair_photos(
    link_photo: str, count_likes: int, id_dating_user: int
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
        return 'Фото пользователя сохранено в избранном'
    except (IntegrityError, InvalidRequestError):
        return 'Фото уже сохранено'


def add_pair_to_favorites(
    vk_id: int, first_name: str,
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
        return 'ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ'
    except (IntegrityError, InvalidRequestError):
        return 'Пользователь уже в избранном.'


def add_pair_to_blacklist(
    vk_id: int, first_name: str,
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
        return 'Пользователь успешно заблокирован.'
    except (IntegrityError, InvalidRequestError):
        return 'Пользователь уже в черном списке.'
