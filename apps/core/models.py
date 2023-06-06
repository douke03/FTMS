import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from crum import get_current_user
from sequences import get_next_value


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name=_("created by"),
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="%(app_label)s_%(class)s_modified_by",
        verbose_name=_("modified by"),
    )
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        user = get_current_user()
        # Conditional branch to create a super user.
        if user is None:
            user = self
        if self.created_date == self.modified_date:
            self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)
        # Conditional branch to create a super user.
        if get_current_user() is not None:
            # Create a personal team if one does not exist.
            if not (
                TeamMember.objects.filter(user=self)
                .filter(team__is_personal=True)
                .exists()
            ):
                personalTeam = Team.objects.create(name=self.username, is_personal=True)
                TeamMember.objects.create(
                    user=self, team=personalTeam, is_team_admin=True
                )


class CommonItem(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name=_("created by"),
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="%(app_label)s_%(class)s_modified_by",
        verbose_name=_("modified by"),
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self.created_date == self.modified_date:
            self.created_by = user
        self.modified_by = user
        super().save(*args, **kwargs)


class Team(CommonItem):
    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    name = models.CharField(max_length=80, verbose_name=_("team name"))
    is_public = models.BooleanField(default=False, verbose_name=_("public"))
    is_personal = models.BooleanField(
        default=False, editable=False, verbose_name=_("personal")
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.created_date == self.modified_date:
            if not self.is_personal:
                # Create a TeamMember when creating a team.
                TeamMember.objects.create(
                    user=get_current_user(), team=self, is_team_admin=True
                )


class TeamMember(CommonItem):
    class Meta:
        verbose_name = _("team member")
        verbose_name_plural = _("team members")

    number = models.IntegerField(editable=False, verbose_name=_("#"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("team"))
    is_team_admin = models.BooleanField(default=False, verbose_name=_("team admin"))

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        self.number = get_next_value("model_team_member_seq")
        super().save(*args, **kwargs)


class Task(CommonItem):
    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

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
    number = models.IntegerField(editable=False, verbose_name=_("#"))
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=NOT_READY,
        verbose_name=_("status"),
    )
    due_date = models.DateField(blank=True, null=True, verbose_name=_("due date"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    estimated_man_hour = models.TimeField(
        blank=True, null=True, verbose_name=_("estimated man hour")
    )
    actual_man_hour = models.TimeField(
        blank=True, null=True, verbose_name=_("actual man hour")
    )
    owner = models.TimeField(blank=True, null=True, verbose_name=_("owner"))

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.number = get_next_value("model_task_seq")
        super().save(*args, **kwargs)
