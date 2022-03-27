from vkinder.settings import engine, Base

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


# Подключение к БД
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()


class User(Base):
    """ Пользователь бота ВК """
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)


class DatingUser(Base):
    """ Анкеты добавленные в избранное """
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))

    __tablename__ = 'dating_user'
    __table_args__ = (
        sq.UniqueConstraint('vk_id', 'user_id', name="unique__dating_user__vk_id__user_id"),
    )


class BlackList(Base):
    """ Анкеты в черном списке """
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))

    __tablename__ = 'black_list'
    __table_args__ = (
        sq.UniqueConstraint('vk_id', 'user_id', name="unique__black_list__vk_id__user_id"),
    )


def create_all(**options):
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all()
