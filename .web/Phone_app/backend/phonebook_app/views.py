from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from phonebook_app import models, serializers


@permission_classes([AllowAny])
def home(request) -> HttpResponse:
    try:
        return render(
            request,
            "index.html",
            context={},
        )
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_person_info(request: Request, person_id=None):
    try:
        person_id = request.query_params.get("person_id")
        if person_id is not None:
            person = models.Person.objects.get(pk=person_id)
            serializer = serializers.PersonSerializer(person)
        else:
            people = models.Person.objects.all().order_by("surname")
            serializer = serializers.PersonSerializer(people, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except models.Person.DoesNotExist:
        return Response(
            data={"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_person_info_jinja(request):
    try:
        people = models.Person.objects.all().order_by("surname")
        serializer = serializers.PersonSerializer(people, many=True)
        return render(request, "person_list.html", {"people": serializer.data})

    except models.Person.DoesNotExist:
        return render(
            request,
            "error.html",
            {"error_message": "Person not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        return render(
            request,
            "error.html",
            {"error_message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
