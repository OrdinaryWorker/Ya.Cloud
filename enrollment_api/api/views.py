from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer
from enrollment_api.settings import logger
from .treatment_functions import (check_not_valid_serializer, check_response,
                                  get_children, update_file, update_parents)


@api_view(['POST'])
def file_imports(request):
    if not check_response(request):

        return Response(status=status.HTTP_400_BAD_REQUEST)

    items_list = []
    items = request.data['items']

    for i in range(len(items)):
        item_dict = items[i]
        item_dict["date"] = request.data["updateDate"]
        serializer = FileSerializer(data=item_dict)
        if serializer.is_valid():
            item = serializer.save()
            if not item:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )
            logger.info('В базу данных добавлена запись')
        else:
            if check_not_valid_serializer(item_dict):
                flag = False
                item = update_file(flag, item_dict)
                if not item:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
                logger.info('В базу данных добавлена запись')
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST
                                )
        flag = True
        update_parents(flag, item, item.size, item.date)
        items_list.append(item_dict)
    return Response(items_list,
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def file_nodes(request, pk):
    try:
        item = File.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FileSerializer(item)
    if item.type == 'FOLDER':
        item_dict = dict(serializer.data)
        item_dict['children'] = get_children(item)
    else:
        item_dict = serializer.data
    return Response(item_dict, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def file_delete(request, pk):
    logger.info('Отправлен запрос на удаление файла')
    flag = False
    try:
        item = File.objects.get(id=pk)
    except ObjectDoesNotExist:
        message = "Item not found"
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    date = request.query_params.get("date")
    if not date:
        message = 'Validation Failed'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    item.date = date
    try:
        item.save()
    except ValidationError:
        message = 'Validation Error'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    logger.info('Запрос прошел валидацию')
    update_parents(flag, item, item.size, item.date)
    item.delete()
    logger.info('Из базы данных удалена запись')
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def files_updates(request):
    logger.info('Отправлен запрос на updates/')
    try:
        date = request.query_params["date"]
    except KeyError:
        message = 'Validation Error for date field'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    end_time = datetime.strptime(date,
                                 "%Y-%m-%dT%H:%M:%SZ")
    start_time = end_time - timedelta(hours=24)
    files = File.objects.filter(
        type='FILE',
        date__range=[start_time, end_time]
    )
    serializer = FileSerializer(files, many=True)
    logger.info('Запрос на updates/ успешно обработан')
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def file_history(request, pk):
    logger.info('Отправлен запрос на history/')
    file = get_object_or_404(File, id=pk)

    start_time = request.data.get("dateStart")
    end_time = request.data.get("dateEnd")
    if start_time and end_time:
        if file.changes_history:
            versions = File.objects.filter(
                new_file_version=pk,
                date__range=[start_time, end_time]
            )
            serializer = FileSerializer(versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        message = 'Validation Error'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    logger.info('Запрос на updates/ успешно обработан')
    return Response(status=status.HTTP_400_BAD_REQUEST)
