import datetime
import json

from db.tuple_models import Photo


def sort_photo(photos: list[Photo]) -> list[Photo]:
    """ Сортируем фото по лайкам, удаляем лишние элементы """
    result = []
    for photo in photos:
        if photo.photo:
            result.append(photo)
    return sorted(result, key=lambda photo: photo.popular)


def json_create(lst):
    """ JSON file create with result of programm """
    today = datetime.date.today()
    res = {}
    res_list = []
    for info in lst:
        res['date'] = str(today)
        res['first_name'] = info[0]
        res['last_name'] = info[1]
        res['link'] = info[2]
        res['id'] = info[3]
        res_list.append(res.copy())

    with open("result.json", "a", encoding='UTF-8') as write_file:
        json.dump(res_list, write_file, ensure_ascii=False)

    print(f'Информация о загруженных файлах успешно записана в json файл.')
