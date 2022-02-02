from django.db import models
from user.models import User


class Note(models.Model):
    """
    this class is created for adding the table in database
    """
    title = models.CharField(max_length=50)
    description =models.CharField(max_length=400)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
