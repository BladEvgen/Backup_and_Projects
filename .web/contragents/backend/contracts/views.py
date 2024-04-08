from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from contracts import models, serializers, utils
from contracts.utils import gin_log_decorator


class CustomLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return redirect("/swagger/")


Cache = caches["default"]


def get_cache(
    key: str, query: callable = lambda: any, timeout: int = 10, cache: any = Cache
) -> any:
    data = cache.get(key)
    if data is None:
        data = query()
        cache.set(key, data, timeout)
    return data


@permission_classes([AllowAny])
@gin_log_decorator
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


@swagger_auto_schema(
    method="POST",
    operation_summary="Allow users to register",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="The user's email address."
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="The user's password."
            ),
        },
        required=["email", "password"],
    ),
    responses={
        201: openapi.Response(
            "User successfully registered",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="A message indicating the outcome of the registration.",
                    ),
                },
            ),
        ),
        400: "BAD REQUEST - Invalid request data or email already in use",
    },
    operation_description="Registers a new user.",
)
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
@gin_log_decorator
def user_register(request):
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if not email or not password:
        return Response(
            {"message": "Требуются адрес электронной почты и пароль"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not utils.password_check(password):
        return Response(
            {"message": "Пароль недействителен"}, status=status.HTTP_400_BAD_REQUEST
        )

    username = email.split("@")[0]
    user, created = User.objects.get_or_create(username=username, email=email)

    if not created:
        return Response(
            {"message": "Данная почта уже занята"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(password)
    user.save()

    return Response(
        {"message": "Пользователь успешно зарегистрирован"},
        status=status.HTTP_201_CREATED,
    )


@swagger_auto_schema(
    method="GET",
    operation_summary="Return data for user",
    responses={
        200: openapi.Response(
            "User details retrieved successfully",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING, description="The user's username."
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The user's email address.",
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The user's first name (optional).",
                    ),
                    "last_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The user's last name (optional).",
                    ),
                },
            ),
        ),
    },
    operation_description="Retrieves details of the currently authenticated user.",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user

    response_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_summary="Retrieves a list of contracts",
    operation_description="Retrieves a list of contracts. Requires authentication.",
    responses={
        200: openapi.Response(
            description="Contracts retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="The ID of the contract.",
                                ),
                                "agent": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="The name of the agent associated with the contract.",
                                ),
                                "total": openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="The total amount of the contract.",
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
    },
)
@swagger_auto_schema(
    method="POST",
    operation_summary="Creates a new contract",
    operation_description="Creates a new contract. Requires authentication.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["agent_id", "total", "file"],
        properties={
            "agent_id": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="The ID of the agent associated with the contract. (Required)",
            ),
            "total": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="The total amount of the contract. (Required)",
            ),
            "comment": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="An optional comment for the contract.",
            ),
            "file": openapi.Schema(
                type=openapi.TYPE_FILE,
                description="An optional file to upload associated with the contract. (Required)",
            ),
        },
    ),
    responses={
        201: openapi.Response(
            description="Contract created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="The ID of the newly created contract.",
                            ),
                            "status": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="The status of the contract (always 'Created' upon creation).",
                            ),
                        },
                    ),
                },
            ),
        ),
        400: "Bad request",
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
@gin_log_decorator
def contracts(request):
    if request.method == "GET":

        def get_contracts():
            return models.Contract.objects.all()

        contracts = get_cache(key="contracts_list", query=get_contracts, timeout=1)

        serializer = serializers.ContractSerializer(contracts, many=True)
        return Response({"data": serializer.data})
    elif request.method == "POST":
        try:
            agent_id = request.data.get("agent_id")
            total = request.data.get("total")
            comment_text = request.data.get("comment")
            file = request.FILES.get("file")

            agent: models.Contragent = get_object_or_404(models.Contragent, pk=agent_id)
            comment: models.Comment = models.Comment.objects.create(
                comment=comment_text
            )
            contract: models.Contract = models.Contract.objects.create(
                agent=agent,
                total=total,
                comment=comment,
                file=file,
            )

            response_data = {"data": {"id": contract.id, "status": "Created"}}
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["GET"],
    operation_id="Get_List_of_Agents",
    responses={
        200: openapi.Response(
            description="List of agents",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "bin": openapi.Schema(type=openapi.TYPE_STRING),
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                },
            ),
        ),
        500: "Internal Server Error",
    },
)
@swagger_auto_schema(
    methods=["POST"],
    operation_id="Create_New_Agent",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "bin": openapi.Schema(type=openapi.TYPE_STRING),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["bin", "title"],
    ),
    responses={
        201: openapi.Response(
            description="New agent created",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "bin": openapi.Schema(type=openapi.TYPE_STRING),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                },
            ),
        ),
        400: "Bad Request",
        500: "Internal Server Error",
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@gin_log_decorator
def agents_detail(request, id=None) -> Response:
    try:
        if request.method == "GET":
            if id is None:

                def get_agents():
                    return models.Contragent.objects.all()

                agents = get_cache(key="agents_list", query=get_agents, timeout=10)

                serialized_agents = [
                    {"id": agent.id, "bin": agent.bin, "title": agent.title}
                    for agent in agents
                ]
                return Response({"data": serialized_agents}, status=status.HTTP_200_OK)

            else:
                agent = models.Contragent.objects.get(pk=id)
                serialized_agent = {
                    "id": agent.id,
                    "bin": agent.bin,
                    "title": agent.title,
                }
                return Response({"data": serialized_agent}, status=status.HTTP_200_OK)

        elif request.method == "POST":
            bin = request.data.get("bin")
            title = request.data.get("title")
            if bin and title:
                agent = models.Contragent.objects.create(bin=bin, title=title)
                serialized_agent = {
                    "id": agent.id,
                    "bin": agent.bin,
                    "title": agent.title,
                }
                return Response(
                    {"data": serialized_agent}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "bin и title обязательные поля"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    except models.Contragent.DoesNotExist:
        return Response(
            {"message": "Агент не существует"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as error:
        return Response(
            {"message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
