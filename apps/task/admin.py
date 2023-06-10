from django.contrib import admin
from .models import Roadmap, Milestone, Task

admin.site.register(Roadmap)
admin.site.register(Milestone)
admin.site.register(Task)
