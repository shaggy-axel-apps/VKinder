from db.tuple_models import Photo


def sort_photo(photos: list[Photo]) -> list[Photo]:
    """ Сортируем фото по лайкам, удаляем лишние элементы """
    result = []
    for photo in photos:
        if photo.photo:
            result.append(photo)
    return sorted(result, key=lambda photo: photo.popular, reverse=True)
