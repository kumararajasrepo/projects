from django.contrib import admin

from task_list.models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "is_completed")


admin.site.register(Task, TaskAdmin)
