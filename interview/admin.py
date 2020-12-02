from django.contrib import admin
from interview.models import Candidate
from django.http import HttpResponse
import csv
from datetime import datetime
import logging
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

# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    #不显示
    exclude = ("creator", "created_date", "modified_date")
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

    #分组显示
    fieldsets = (
        (None, {"fields": ("userid", ("username", "city", "phone"), "email", "apply_position", "born_address", "gender", "candidate_remark", "bachelor_school", "master_school", "doctor_school", "major", "degree", "test_score_of_general_ability", "paper_score",)}),
        ("第一面", {"fields": ("first_score", "first_learning_ability", "first_professional_competency", "first_advantage", "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",)}),
        ("第二面", {"fields": ("second_score", "second_learning_ability", "second_professional_competency", "second_pursue_of_excellence", "second_communication_ability", "second_pressure_score", "second_advantage", "second_disadvantage", "second_result", "second_recommend_position", "second_interviewer_user", "second_remark",)}),
        ("第三面", {"fields": ("hr_score", "hr_responsibility", "hr_communication_ability", "hr_logic_ability", "hr_potential", "hr_stability", "hr_advantage", "hr_disadvantage", "hr_result", "hr_interviewer_user", "hr_remark",)})
    )

    actions = [export_model_as_csv]
admin.site.register(Candidate, CandidateAdmin)
