from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import CommonItem, Team
from sequences import get_next_value


class Roadmap(CommonItem):
    class Meta:
        verbose_name = _("roadmap")
        verbose_name_plural = _("roadmaps")

    roadmap = models.CharField(max_length=80, verbose_name=_("roadmap"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))

    def __str__(self):
        return self.roadmap


class Milestone(CommonItem):
    class Meta:
        verbose_name = _("milestone")
        verbose_name_plural = _("milestones")

    milestone = models.CharField(max_length=80, verbose_name=_("milestone"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("roadmap"),
    )

    def __str__(self):
        return self.milestone

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Task.objects.filter(milestone=self).update(roadmap=self.roadmap)


class Task(CommonItem):
    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    NOT_READY = "NOT_READY"
    READY = "READY"
    DOING = "DOING"
    DONE = "DONE"
    STATUS_CHOICES = [
        (NOT_READY, "Not Ready"),
        (READY, "Ready"),
        (DOING, "Doing"),
        (DONE, "Done"),
    ]
    MAN_HOUR = [
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (8, 8),
    ]
    number = models.IntegerField(editable=False, verbose_name=_("#"))
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    owner = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        verbose_name=_("owner"),
    )
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=NOT_READY,
        verbose_name=_("status"),
    )
    due_date = models.DateField(blank=True, null=True, verbose_name=_("due date"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("end date"))
    estimated_man_hour = models.IntegerField(
        choices=MAN_HOUR,
        default=1,
        verbose_name=_("estimated man hour"),
    )
    actual_man_hour = models.IntegerField(
        blank=True, null=True, verbose_name=_("actual man hour")
    )
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("roadmap"),
    )
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("milestone"),
    )

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.number = get_next_value("model_task_seq")
        if self.milestone:
            if self.milestone.roadmap:
                self.roadmap = self.milestone.roadmap
        super().save(*args, **kwargs)
