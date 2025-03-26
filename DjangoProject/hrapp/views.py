from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from hrapp.models.models import *
from hrapp.models.CustomModels import *
from django.http import JsonResponse
from .utils import load_evaluations, generate_prompt_and_summary
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import load_evaluations, generate_prompt_and_summary

# Create your views here.
def index(request):
    schedules = Schedules.objects.active_schedules()
    return render(request,"sample.html",{"schedules":schedules})

#def schedules_view(request):
    #schedules = Schedules.objects.active_schedules()
    #return render(request, "sample.html", {"schedules": schedules})
def schedule_view(request):
    schedules = Schedules.objects.active_schedules()
    courses = list(Courses.objects.filter(is_active=1).values_list("name", flat=True))  # Get only active courses
    print("Courses data:", courses)  # Debugging output
    return render(request, "sample.html", {"schedules": schedules, "courses": courses})







@api_view(['GET'])
def generate_observation_summary(request):
    try:
        evaluations_data = load_evaluations()
        feedback_csv_path = "feedback.csv"  # Replace with the actual path
        summary = generate_prompt_and_summary(evaluations_data, feedback_csv_path)

        return Response({"summary": summary})  # ✅ DRF Response
    except Exception as e:
        return Response({"error": str(e)}, status=500)

