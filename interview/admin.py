from django.contrib import admin
from interview.models import Candidate
from django.http import HttpResponse
import csv
from datetime import datetime
import logging
from django.db.models import Q
from interview import candidate_filedset as cf
from interview import dingtalk
logging = logging.getLogger(__name__)


exportable_fields = ("username", "city", "bachelor_school",
                    "first_score", "first_result", "first_interviewer_user",
                    "second_score", "second_result", "second_interviewer_user",
                    "hr_score", "hr_result", "hr_interviewer_user",
                    "last_editor"
                )


def export_model_as_csv(model_admin, request, queryset):
    response = HttpResponse(content="text/csv")
    fields_list = exportable_fields
    response["Content-Disposition"] = "attachment; filename=recruitment-candidates-list-%s.csv"%datetime.now().strftime("%Y-%m-%d %H:%M%S")

    writer = csv.writer(response)
    writer.writerow([queryset.model._meta.get_field(i).verbose_name.title() for i in fields_list])
    for obj in queryset:
        csv_line_values = []
        for field in fields_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logging.info("%s exported %s candidate records"%(request.user, len(queryset)))
    return response


export_model_as_csv.short_description = "导出csv"
export_model_as_csv.allowed_permissions = ('export', )

# 通知面试官面试
def notify_interviewer(model_admin, request, queryset):
    candidate = ''
    interviewer = ''
    for obj in queryset:
        candidate = obj.username + ';' + candidate
        interviewer = obj.first_interviewer_user.username + ';' + interviewer
    dingtalk.send(f"候选人 {candidate} 进入面试环节 面试官 {interviewer}", ['18140047023'])
notify_interviewer.short_description = "通知面试官"



# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    #不显示
    exclude = ("creator", "created_date", "modified_date")
    actions = (export_model_as_csv, notify_interviewer)

    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm(f'{opts.app_label}.export')

    #显示
    list_display = ("username", "city", "bachelor_school",
                    "first_score", "first_result", "first_interviewer_user",
                    "second_score", "second_result", "second_interviewer_user",
                    "hr_score", "hr_result", "hr_interviewer_user",
                    "last_editor"
                )

    # 搜索
    search_fields = ("username", "phone", "email", "bachelor_school")

    # 筛选条件
    list_filter = ("city", "first_result", "second_result", "hr_result", "first_disadvantage", "second_disadvantage", "hr_disadvantage")

    # 排序
    ordering = ("hr_result", "second_result", "first_result")

    # 页面批量修改
    # list_editable = ("first_interviewer_user", "second_interviewer_user")
    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return ("first_interviewer_user", "second_interviewer_user")
        else:
            return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 设置只读字段
    # readonly_fields = ("first_interviewer_user", "second_interviewer_user")
    default_readonly_fields = ("first_interviewer_user", "second_interviewer_user")
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            return self.default_readonly_fields

        return ()

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            # 获取用户的组
            group_names.append(g.name)
        return group_names

    # 数据集的权限限制，只能看自己面试的人
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs

        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )


    # 分组显示
    # fieldsets = cf.default_fieldsets

    # 一面面试官只能填写一面内容，二面只能二面
    def get_fieldsets(self, request, obj=None):
        group_name = self.get_group_names(request.user)
        if 'interviewer' in group_name and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_name and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets



admin.site.register(Candidate, CandidateAdmin)
