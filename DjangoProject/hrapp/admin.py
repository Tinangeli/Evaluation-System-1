from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Schedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'professor', 'subject', 'room', 'name', 'time', 'semester', 'year', 'is_active')
    list_filter = ('semester', 'year', 'is_active')
    search_fields = ('name', 'course__name', 'professor__name', 'subject__name')
    ordering = ('-created_at',)


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id',"name", 'code', 'is_active', 'created_at', 'updated_at')

@admin.register(Evaluations)
class EvaluationsAdmin(admin.ModelAdmin):
    list_display = ('id',"dean", 'schedule', 'observation_date', 'evaluation_type',"additional_comments",'student_activities','instructor_activities')

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id',"name", 'is_active')

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id',"name" , 'is_active')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id',"name", 'email', 'email_verified_at', 'password', 'remember_token')

@admin.register(UserUser)
class Admin(admin.ModelAdmin):
        list_display = ('id', "parent","child")

