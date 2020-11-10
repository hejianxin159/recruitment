from django.urls import path
from django.conf.urls import url
from jobs import views


urlpatterns = [
    url(r"^joblist/", views.job_list, name="joblist")
]
