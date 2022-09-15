import random
from django.core.exceptions import ObjectDoesNotExist

from .models import File
from .serializers import FileSerializer


def check_response(request) -> bool:
    """Функция проверяет наличие обязательных ключей в теле запроса"""
    try:
        request.data["items"]
    except KeyError:
        return False
    try:
        request.data["updateDate"]
    except KeyError:
        return False
    if not isinstance(request.data["items"], list):
        return False
    return True


def check_not_valid_serializer(item_dict: dict) -> bool:
    """Функция осуществляет дополнительную проверку входных данных в случае,
    если сериализатор нашел ошибку, выполняется перед запуском
     обновления файла"""
    try:
        pk = item_dict['id']
    except KeyError:
        return None
    try:
        item_type = item_dict['type']
    except KeyError:
        return None
    return (File.objects.filter(id=pk).exists() and
            File.objects.get(id=pk).type == item_type)


def get_children(item: File) -> list:
    """Функция рекуррентно проходит по файлам у которых parentId = id файла
    и добавляет их в список для вывода"""
    children = File.objects.filter(parentId=item.pk)
    child_list = []
    for child in children:
        if child.type == 'FILE':
            child_serializer = FileSerializer(child)
            child_dict = dict(child_serializer.data)
            child_dict['children'] = None
            child_list.append(child_dict)
        else:
            child_serializer = FileSerializer(child)
            child_dict = dict(child_serializer.data)
            child_dict['children'] = get_children(child)
            child_list.append(child_dict)
    return child_list


def update_file(flag, new_item):
    """Функция замены текущей версии файла на новую версию и добавляет в
     атрибут changes_history ссылку на объект старой версии файла"""
    current_id = new_item['id']
    new_id = get_hash_id(current_id)
    new_item['id'] = new_id

    serializer = FileSerializer(data=new_item)
    if not serializer.is_valid():
        return None
    serializer.save()
    previous_version_file = File.objects.get(id=current_id)
    update_version_file = File.objects.get(id=new_id)
    prev_file_data, upd_file_data = do_files_tuple_changing(
        previous_version_file,
        update_version_file)
    upd_serializer = FileSerializer(data=upd_file_data)
    prev_serializer = FileSerializer(data=prev_file_data)
    update_parents(flag,
                   previous_version_file,
                   previous_version_file.size,
                   previous_version_file.date)
    previous_version_file.delete()
    update_version_file.delete()
    if upd_serializer.is_valid() and prev_serializer.is_valid():
        prev_file = upd_serializer.save()
        updated_file = prev_serializer.save(changes_history=prev_file)
        return updated_file
    return None


def update_parents(flag, obj, size, date):
    """Функция обновляет параметры size и date у родительских объектов файла"""
    try:
        parent_item = File.objects.get(id=obj.parentId_id)
    except ObjectDoesNotExist:
        parent_item = None
    if parent_item:

        if obj.size is not None:
            if parent_item.size is None:
                parent_item.size = 0
            if flag:
                parent_item.size += size
                parent_item.date = date
            else:
                parent_item.size -= size
                parent_item.date = date
        parent_item.save()
        return update_parents(flag, parent_item, size, date)
    return parent_item


def get_hash_id(item_id):
    """Функция создает уникальный id для старых версий файлов"""
    return str(hash(item_id + str(random.randint(0, 1000))))


def do_files_tuple_changing(prev_file, upd_file):
    """Функция перезаписывает атрибуты новой версии файла в уже существующую
     версию и возвращает списки с соответствующими атрибутами"""
    prev_serializer = FileSerializer(prev_file)
    upd_serializer = FileSerializer(upd_file)
    prev = dict(prev_serializer.data)
    upd = dict(upd_serializer.data)

    prev['url'], upd['url'], = upd['url'], prev['url']
    prev['size'], upd['size'], = upd['size'], prev['size']
    prev['parentId'], upd['parentId'], = upd['parentId'], prev['parentId']
    prev['date'], upd['date'] = upd['date'],  prev['date']

    upd['parentId'] = None
    return prev, upd
