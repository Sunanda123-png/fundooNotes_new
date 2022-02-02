import pytest
from rest_framework.reverse import reverse
from user.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUser:
    def test_user_registration(self, client):
        # test case create their own database to test the views
        url = reverse("user_registration")
        user = {
            "username": "sunanda",
            "password": "root",
            "age": 24,
            "email": "ssunanda02@gmail.com",
            "first_name": "sunanda",
            "last_name": "shil",
            "is_verified": 0
        }
        response = client.post(url, user)
        assert response.status_code == 201

    def test_user_is_verified_should_login(self, client):
        #test the login
        user = User.objects.create_user("sunanda",
                                        password="root",
                                        age=24,
                                        email="ssunanda02@gmail.com",
                                        first_name="sunanda",
                                        last_name="shil",
                                        is_verified=0)
        user.is_verified = True
        user.save()
        data = {
            "username": "sunanda",
            "password": "root",
        }
        url = reverse("login")
        response = client.post(url, data)
        assert response.status_code == 200
