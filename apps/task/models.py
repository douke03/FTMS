from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import CommonItem
from sequences import get_next_value

# Create your models here.


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
