from django.shortcuts import render
from django.views import View
from jobs.models import Job
from django.template import loader
from jobs.models import cities, job_types
from django.http import HttpResponse
# Create your views here.

# class JobList(View):
#     def get(self, request):
#         job_list = Job.objects.order_by("job_type")
#         template =

def job_list(request):
    job_list = Job.objects.order_by("job_type")
    template = loader.get_template("joblist.html")
    context = {"job_list": job_list}
    for job in job_list:
        job.job_city = cities[job.job_city][1]
        job.job_type = job_types[job.job_type][1]

    return HttpResponse(template.render(context))