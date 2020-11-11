from django.contrib import admin
from jobs.models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    #不显示
    exclude = ("creator", "created_date", "modified_date")
    list_display = ("job_name", "job_type", "job_city", "creator", "created_date", "modified_date")

    def save_model(self, request, obj, form, change):
        # 保存model时自动添加创建者
        obj.creator = request.user
        super(JobAdmin, self).save_model(request, obj, form, change)



admin.site.register(Job, JobAdmin)
