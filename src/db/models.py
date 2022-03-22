from vkinder.settings import DB_CREDS

import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# Подключение к БД
Base = declarative_base()

engine = sq.create_engine(
    ('postgresql://'
     f'{DB_CREDS["USER"]}:{DB_CREDS["PASS"]}@'
     f'{DB_CREDS["HOST"]}:{DB_CREDS["PORT"]}/'
     f'{DB_CREDS["NAME"]}'),
    client_encoding='utf8')
Session = sessionmaker(bind=engine)

# Для работы с ВК

# Для работы с БД
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
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


class Photos(Base):
    """ Фото избранных анкет """
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_dating_user = sq.Column(sq.Integer, sq.ForeignKey('dating_user.id', ondelete='CASCADE'))


class BlackList(Base):
    """ Анкеты в черном списке """
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
