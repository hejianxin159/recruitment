from django.shortcuts import render
from django.views import View
from jobs.models import Job
from django.template import loader
from jobs.models import Cities, JobTypes
from django.http import HttpResponse
from django.http import Http404
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
        job.job_city = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    return HttpResponse(template.render(context))


def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("job not exist")

    return render(request, "job.html", {"job": job})