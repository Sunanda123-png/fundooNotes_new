import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from rest_framework.response import Response
from user.utils import EncodeDecodeToken

from .redis import RedisCode


class Cache:
    """
    this class is created for caching which user try to access frequently
    """

    def add_note_to_cache(self, user_id, note):
        """
        for adding the note in catch
        :param user_id: user_id of the person
        :param note: note details
        :return: id and data
        """
        try:
            note_list = RedisCode().get(user_id)
            if note_list is None:
                RedisCode().cache.set(user_id, json.dumps([note]))
            else:
                note_list = json.loads(note_list)
                note_list.append(note)
                RedisCode().cache.set(user_id, json.dumps(note_list))
                return
        except Exception as e:
            logging.error(e)

    def get_note_from_cache(self, user_id):
        """
        for geting note from catch
        :param user_id: user_id of the person
        :return: user_id
        """
        try:
            RedisCode().cache.get(user_id)
        except Exception as e:
            raise e

    def update_note_to_cache(self, user_id, updatednote):
        """
        for updating the note in cache
        :param user_id: id of note
        :param updatednote: note details
        """
        note_list = RedisCode().get(user_id)
        if note_list is None:
            RedisCode().cache.set(user_id, json.dumps([updatednote]))
            return
        for note in note_list:
            if updatednote.get(id) == note.get(id):
                note.update(updatednote)
                return

        else:
            raise ObjectDoesNotExist

    def delete_note_to_cache(self, user_id, note_id):
        """
        for deleting the note from cache
        :param user_id: user id
        :param note_id: id of the note
        :return: note
        """
        note_list = RedisCode().cache.get(user_id)
        if note_list is None:
            raise ObjectDoesNotExist
        for note in note_list:
            if RedisCode().cache.get(note_id) == note.get(id):
                del (note)
                return
        else:
            raise ObjectDoesNotExist


def verify_token(function):
    """
    this function is created for verifying user
    """
    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            logging.info('Token not provided in the header')
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data.update({'user_id': user_id["user_id"]})
        return function(self, request)

    return wrapper
