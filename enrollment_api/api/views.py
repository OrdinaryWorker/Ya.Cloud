from django.core.exceptions import ObjectDoesNotExist,ValidationError
from .serializers import FileSerializer
from .models import File
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework import status


@api_view(['POST'])
def file_imports(request):
    items = request.data.get("items")
    items_list = []
    if isinstance(items, list):
        for i in range(len(items)):
            item_dict = items[i]
            item_dict["date"] = request.data["updateDate"]
            items_list.append(item_dict)
            serializer = FileSerializer(data=item_dict)
            if serializer.is_valid():
                item = serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )
            update_parents(request, item, item.size, item.date)
        return Response(items_list,
                        status=status.HTTP_200_OK)
    else:
        message = 'Введены некорректные данные'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


def update_parents(request, obj, size, date):
    try:
        parent_item = File.objects.get(id=obj.parentId_id)
    except ObjectDoesNotExist:
        parent_item = None
    if parent_item:

        if obj.size is not None:
            if parent_item.size is None:
                parent_item.size = 0
            if request.method == 'POST':
                parent_item.size += size
                parent_item.date = date
            else:
                parent_item.size -= size
                parent_item.date = date
        parent_item.save()
        return update_parents(request, parent_item, size, date)
    return parent_item


@api_view(['GET'])
def files_nodes(request):
    items = File.objects.all()
    serializer = FileSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def file_nodes(request, pk):
    item = File.objects.get(id=pk)
    serializer = FileSerializer(item)
    if item.type == 'FOLDER':
        item_dict = dict(serializer.data)
        item_dict['children'] = get_children(item)
    else:
        item_dict = serializer.data
    return Response(item_dict, status=status.HTTP_200_OK)


def get_children(item):
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


@api_view(['DELETE'])
def file_delete(request, pk):
    try:
        item = File.objects.get(id=pk)
    except ObjectDoesNotExist:
        message = "Item not found"
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    date = request.data.get("date")
    if not date:
        message = 'Validation Failed'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    item.date = date
    try:
        item.save()
    except ValidationError:
        message = 'Validation Error for date field'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    update_parents(request, item, item.size, item.date)
    item.delete()
    return Response(status=status.HTTP_200_OK)