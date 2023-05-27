from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Team, Member, Task

CustomUser = get_user_model()
admin.site.register(CustomUser)
admin.site.register(Team)
admin.site.register(Member)
admin.site.register(Task)
