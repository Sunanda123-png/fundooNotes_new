import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from notes.models import Note
from notes.serializers import NotesSerializer
from notes.utility import verify_token


logging.basicConfig(filename="views.log", filemode="w")


class Notes(APIView):
    """
    class based views for crud operation
    """

    @swagger_auto_schema(
        operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
            }
        ),
        )
    @verify_token
    def post(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Cache().add_note_to_cache(request.data.get("user_id"),serializer.data)
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Data not stored"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="fetch notes",
    )
    @verify_token
    def get(self, request):
        """
        this method is created for retrieve data
        :param request: format of the request
        :return: Response
        """
        try:
            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(note, many=True)
            # Cache().get_note_from_cache(user_id=request.GET.get("user_id"))
            return Response(
                {
                    "message": "Here your Note",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            logging.error(e)
            return Response(
                {
                    "message": "No notes for you"
                },
                status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note id"),
            }
        ),
    )
    @verify_token
    def put(self, request):
        """
        this method is created for update the data
        :param request: format of the request
        :return: Response
        """
        try:
            note = Note.objects.get(id=request.data["id"])
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Cache().add_note_to_cache(request.data.get("user_id"), serializer.data)
            return Response(
                {
                    "message": "Data updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)
        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "Data not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "no such note found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_summary="Delete notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note id"),
            }
        ),
    )
    @verify_token
    def delete(self, request):
        """
        this method is created for delete the note
        :param request:format of the request
        :return: response
        """
        try:
            note = Note.objects.get(pk=request.data["id"])
            note.delete()
            # Cache().delete_note_to_cache(request.data.get("user_id"),request.data.get("id"))
            return Response(
                {
                    "message": "Data deleted"
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)
