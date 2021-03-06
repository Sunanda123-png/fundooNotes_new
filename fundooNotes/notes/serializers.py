from rest_framework import serializers
from .models import Note


class NotesSerializer(serializers.ModelSerializer):
    """
        Serializer is used to converting the json data
    """

    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validate_data):
        """
        for creating the notes
        :param validate_data: validating the api data
        """
        notes = Note.objects.create(
            title=validate_data.get("title"),
            description=validate_data.get("description"),
            user_id=validate_data.get("user_id"),
        )
        return notes
