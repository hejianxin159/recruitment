from django.urls import path
from django.conf.urls import url
from jobs import views


urlpatterns = [
    path("", views.job_list, name="index"),
    url(r"^joblist/", views.job_list, name="joblist"),
    url(r"^job/(?P<job_id>\d+)/$", views.job_detail, name="detail")
]
