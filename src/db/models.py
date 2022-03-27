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
    __tablename__ = 'dating_user'
    __table_args__ = sq.UniqueConstraint('vk_id', 'id_user', name="unique__vk_id__user_id")
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


class BlackList(Base):
    """ Анкеты в черном списке """
    __tablename__ = 'black_list'
    __table_args__ = sq.UniqueConstraint('vk_id', 'id_user', name="unique__vk_id__user_id")
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


def create_all(**options):
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all()
