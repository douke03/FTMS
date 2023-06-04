import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from crum import get_current_user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []


class CommonItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        editable=False,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        related_name="%(app_label)s_%(class)s_last_modified_by",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.created_by_id:
            self.created_by = user
        self.last_modified_by = user
        super().save(*args, **kwargs)


class Team(CommonItem):
    name = models.CharField(max_length=80)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TeamMember(CommonItem):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_team_admin = models.BooleanField(default=False)
    view = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.view

    def save(self, *args, **kwargs):
        self.view = self.team.name + "_" + self.user.username
        super().save(*args, **kwargs)


class Task(CommonItem):
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
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=NOT_READY)
    due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimated_man_hour = models.TimeField(blank=True, null=True)
    actual_man_hour = models.TimeField(blank=True, null=True)
    owner = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
