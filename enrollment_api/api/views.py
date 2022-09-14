from django.core.exceptions import ObjectDoesNotExist
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
            item_dict["updateDate"] = request.data["updateDate"]
            items_list.append(item_dict)
            serializer = FileSerializer(data=item_dict)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )
        
        return Response(items_list,
                        status=status.HTTP_201_CREATED)
    else:
        message = 'Введены некорректные данные'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
        item_dict['children'], item_dict['size'] = get_children(item)
    else:
        item_dict = serializer.data
    return Response(item_dict, status=status.HTTP_200_OK)


def get_children(item):
    children = File.objects.filter(parentId=item.pk)
    item_size = 0
    child_list = []
    for child in children:
        if child.type == 'FILE':
            item_size += int(child.size)
            child_serializer = FileSerializer(child)
            child_dict = dict(child_serializer.data)
            child_list.append(child_dict)
        else:
            child_serializer = FileSerializer(child)
            child_dict = dict(child_serializer.data)
            child_dict['children'], child_dict['size'] = get_children(child)
            item_size += int(child_dict['size'])
            child_list.append(child_dict)
    return child_list, item_size


@api_view(['DELETE'])
def file_delete(request, pk):
    try:
        item = File.objects.get(id=pk)
    except ObjectDoesNotExist:
        message = "Item not found"
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    if request.data.get("date") != item.updateDate:
        message = 'Validation Failed'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_200_OK)
