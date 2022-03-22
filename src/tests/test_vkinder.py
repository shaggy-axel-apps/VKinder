import pytest

from db.queries import add_user, add_user_photos, add_to_black_list
from services.vk_functions import search_users, get_photo
from services.message_handler import register_user
from services.utils import sort_likes


class TestVkinderApp:
    """ Тесты по работе приложения """
    @pytest.mark.parametrize('sex, age_at, age_to, city, result', [
        ('1', '18', '21', 'Москва', True)])
    def test_search_users(self, sex, age_at, age_to, city, result):
        """ Проверка поиска анкет """
        assert search_users(sex, age_at, age_to, city) == result

    @pytest.mark.parametrize('user_id, result', [('336261034', True)])
    def test_get_photo(self, user_id, result):
        """ Тест поиска фотографий """
        assert get_photo(user_id) == result

    @pytest.mark.parametrize('list_photos, result',
                             [(['1', 'photo_1', '2', 'photo_2', '3', 'photo_3'],
                               ['1', '2', '3', 'photo_1', 'photo_2', 'photo_3']), ])
    def test_sort_likes(self, list_photos, result):
        """ Тест сортировки по лайкам """
        assert sort_likes(list_photos) == result


class TestVkinderDB:
    """ Тесты по работе Базы данных """
    @pytest.mark.parametrize('vk_id, result', [('1', False), ('1', False), ('336261034', False)])
    def test_register_user(self, vk_id, result):
        """ Тест первичной регистрации юзера """
        assert register_user(vk_id) == result

    @pytest.mark.parametrize('event_id, vk_id, first_name, last_name, city, link, id_user, result',
                             [('7717001', '2', 'goga', 'boba', 'Turkey', 'www.vkman.ru', '1', False)])
    def test_add_user(self, event_id, vk_id, first_name, last_name, city, link, id_user, result):
        """ Тест добавление пользователя """
        assert add_user(event_id, vk_id, first_name, last_name, city, link, id_user) == result

    @pytest.mark.parametrize('event_id, link_photo, count_likes, id_dating_user, result',
                             [('123', 'link_link', '2', '33502052', False)])
    def test_add_user_photos(self, event_id, link_photo, count_likes, id_dating_user, result):
        """ Тест добавление фото анкеты в БД """
        assert add_user_photos(event_id, link_photo, count_likes, id_dating_user) == result


class TestVkinderBlackList:
    """ Тесты Черного Списка """
    @pytest.mark.parametrize(
        'event_id, vk_id, first_name, last_name, city, link, link_photo, count_likes, id_user, result',
        [('123', '12', '12434', '1251231', 'sdfsdfs', 'sfsdfsdfds', 'fsdfsdfs', '12', '123', False)])
    def test_add_user_to_black_list(
        self, event_id, vk_id, first_name, last_name,
        city, link, link_photo, count_likes,
        id_user, result
    ):
        """ Добавление в черный список """
        assert add_to_black_list(event_id, vk_id, first_name, last_name, city, link, link_photo, count_likes,
                                 id_user) == result
