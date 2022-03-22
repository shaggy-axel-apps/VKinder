import datetime
import json


# Сортируем фото по лайкам, удаляем лишние элементы
def sort_likes(photos):
    result = []
    for element in photos:
        if element != ['нет фото.'] and photos != 'нет доступа к фото':
            result.append(element)
    return sorted(result)


# JSON file create with result of programm
def json_create(lst):
    today = datetime.date.today()
    today_str = f'{today.day}.{today.month}.{today.year}'
    res = {}
    res_list = []
    for info in lst:
        res['data'] = today_str
        res['first_name'] = info[0]
        res['last_name'] = info[1]
        res['link'] = info[2]
        res['id'] = info[3]
        res_list.append(res.copy())

    with open("result.json", "a", encoding='UTF-8') as write_file:
        json.dump(res_list, write_file, ensure_ascii=False)

    print(f'Информация о загруженных файлах успешно записана в json файл.')

