import pytest
import json
from rest_framework.reverse import reverse
from user.models import User
from notes.models import Note

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestNotes:
    def test_to_add_notes_of_particular_user(self, client):
        user = User.objects.create_user("sunanda",
                                        password="root",
                                        age=24,
                                        email="ssunanda02@gmail.com",
                                        first_name="sunanda",
                                        last_name="shil",
                                        is_verified=0)
        user.is_verified = True
        user.save()
        # logging the user
        data = {
            "username": "sunanda",
            "password": "root",
        }
        url = reverse("login")
        response = client.post(url, data)
        json_data = json.loads(response.content)
        print(json_data)
        token = json_data.get('data').get("token")
        # adding notes
        notes_data = {
            "title": "jungle book",
            "description": "nominated for oscar"
        }
        url = reverse("notes")
        header = {
            "HTTP_AUTHORIZATION": token,
        }
        response = client.post(url, notes_data, **header)
        print(response.content)
        assert response.status_code == 201

    def test_to_fetch_note_of_particular_user(self, client):
        user = User.objects.create_user("sunanda",
                                        password="root",
                                        age=24,
                                        email="ssunanda02@gmail.com",
                                        first_name="sunanda",
                                        last_name="shil",
                                        is_verified=0)
        user.is_verified = True
        user.save()
        # logging the user
        data = {
            "username": "sunanda",
            "password": "root",
        }
        url = reverse("login")
        response = client.post(url, data)
        json_data = json.loads(response.content)
        print(json_data)
        token = json_data.get('data').get("token")
        # adding notes
        notes_data = {
            "title": "jungle book",
            "description": "nominated for oscar"
        }
        url = reverse("notes")
        header = {
            "HTTP_AUTHORIZATION": token,
        }
        response = client.get(url, notes_data, **header)
        print(response.content)
        assert response.status_code == 200

    def test_to_update_note_of_particular_user(self, client):
        user = User.objects.create_user("sunanda",
                                        password="root",
                                        age=24,
                                        email="ssunanda02@gmail.com",
                                        first_name="sunanda",
                                        last_name="shil",
                                        is_verified=0)
        user.is_verified = True
        user.save()
        # logging the user
        data = {
            "username": "sunanda",
            "password": "root",
        }
        url = reverse("login")
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        # adding notes
        notes_data = {
            "title": "jungle book",
            "description": "nominated for oscar"
        }
        url = reverse("notes")
        header = {
            "HTTP_AUTHORIZATION": token,
            "content_type": 'application/json'
        }
        response = client.post(url, notes_data, **header)
        print(response.content)
        json_data = json.loads(response.content)
        print(json_data)
        id = json_data.get('data').get("id")
        update_data = {
            "title": "jungle book",
            "description": "nominated for oscar",
            "id":int(id)
        }
        response = client.put(url, update_data,**header)
        assert response.status_code == 202

    def test_to_delete_an_exsisting_note(self, client):

        #creating user
        user = User.objects.create_user("sunanda",
                                        password="root",
                                        age=24,
                                        email="ssunanda02@gmail.com",
                                        first_name="sunanda",
                                        last_name="shil",
                                        is_verified=0)
        user.is_verified = True
        user.save()
        #logging the user
        data = {
            "username": "sunanda",
            "password": "root",
        }
        url = reverse("login")
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data.get('data').get("token")
        # adding notes
        notes_data = {
            "title": "jungle book",
            "description": "nominated for oscar"
        }
        url = reverse("notes")
        header = {
            "HTTP_AUTHORIZATION": token,
            "content_type": 'application/json'
        }
        response = client.post(url, notes_data, **header)
        print(response.content)
        json_data = json.loads(response.content)
        print(json_data)
        id = json_data.get('data').get("id")
        #deleting exsisting note
        delete_note_data = {
            "id":id
        }
        response = client.delete(url, delete_note_data,**header)
        assert response.status_code == 204