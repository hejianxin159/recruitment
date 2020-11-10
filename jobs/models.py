from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
job_types = [
    (0, "技术类"),
    (1, "产品类"),
    (2, "运营类"),
    (3, "设计类")
]
cities = [
    (0, "北京"),
    (1, "上海"),
    (2, "深圳")
]
class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=job_types, verbose_name="职位类别")
    job_name = models.CharField(max_length=200, blank=False, verbose_name="职位名称")
    job_city = models.SmallIntegerField(blank=False, choices=cities, verbose_name="工作地点")
    job_responsibility = models.TextField(max_length=1024, blank=False, verbose_name="职位职责")
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name="职位要求")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    created_date = models.DateField(verbose_name="创建时间", default=datetime.datetime.now)
    modified_date = models.DateField(verbose_name="修改时间", default=datetime.datetime.now)

