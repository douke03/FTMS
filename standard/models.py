import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    REQUIRED_FIELDS = []


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_team_admin = models.BooleanField(default=False)
    view = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.view

    def save(self, *args, **kwargs):
        self.view = self.team.name + "_" + self.user.username
        super().save(*args, **kwargs)


class Task(models.Model):
    NOT_READY = "NOT_READY"
    READY = "READY"
    DOING = "DOING"
    DONE = "DONE"
    STATUS_CHOICES = [
        (NOT_READY, "not Ready"),
        (READY, "Ready"),
        (DOING, "Doing"),
        (DONE, "Done"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=NOT_READY)
    due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimated_man_hour = models.TimeField(blank=True, null=True)
    actual_man_hour = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
