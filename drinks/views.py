from .models import Drink
from .serializer import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def __get_drink_list():
    drinks = Drink.objects.all()
    serializer = DrinkSerializer(drinks, many=True)

    return Response({'drinks': serializer.data})


def __add_drink(req_data):
    serializer = DrinkSerializer(data=req_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def __get_drink_details(drink):
    serializer = DrinkSerializer(drink)
    return Response(serializer.data)


def __update_drink(drink, req_data):
    serializer = DrinkSerializer(drink, data=req_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def __delete_drink(drink):
    drink.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def drinks_list_requests(request, format=None):
    match request.method:
        case 'GET':
            return __get_drink_list()
        case 'POST':
            return __add_drink(request.data)
        case _:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_requests(request, id, format=None):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case 'GET':
            return __get_drink_details(drink)
        case 'PUT':
            return __update_drink(drink, request.data)
        case 'DELETE':
            return __delete_drink(drink)
        case _:
            return Response(status=status.HTTP_404_NOT_FOUND)
