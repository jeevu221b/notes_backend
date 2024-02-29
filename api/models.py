from django.db import models
import uuid


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=150)

    def __str__(self):
        return self.note


class User(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(max_length=30, unique=True, blank=False)
    password = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.username


class Token(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    token = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)
