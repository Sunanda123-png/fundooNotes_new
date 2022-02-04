import logging

from rest_framework.exceptions import ValidationError
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import auth
from user.task import send_mail
from user.utils import EncodeDecodeToken

logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    """
    class based views for User registration
    """

    def post(self, request):
        """
        this method is created for inserting the data
        :param request: format of the request
        :return: Response
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(validate_data=serializer.data)
            send_mail.delay(serializer.data["email"])
            return Response(
                {
                    'message': "Successfully Registered"
                })

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
                    "message": "data storing failed"
                },
                status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        """
        This method is created for user login
        :param request: web request for login the user
        :return:response
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                payload={}
                encoded_token = EncodeDecodeToken.encode_token(user.pk)
                return Response(
                    {
                        "message": "logged in successfully",
                        "data": {"token": encoded_token}
                    }, status=status.HTTP_202_ACCEPTED)
            return Response(
                {
                    "message": "login failed No user"
                },
                status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            logging.error("Authentication failed")
