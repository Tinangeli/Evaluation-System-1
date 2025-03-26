"""REFER TO MODELS.PY FOR INFORMATION AND EDITING ABOUT TABLES

CustomMODELS.PY IS FOR VIEWING DATABASE FOR DJANGO, RETURNS COLUMNS/FIELDS THAT ARE SELECTED,
PUT INSIDE VALUES() TO ADD COLUMNS. VIEW THE MODELS.PY TO LOOK FOR FIELD/COLUMNS NAMES"""
from django.db import models


"""PERMISSIONS/ROLES/USERS/MODELS AND OTHER RELATED TO BELOW"""
class PermissionsManager(models.Manager):
    """RETURNS PERMISSIONS WITH SELECTED FIELDS"""
    def get_queryset(self):
        return self.get_queryset().filter().values("id","name","guard_name")

class RoleHasPermissionsManager(models.Manager):
    """RETURNS ROLESHASPERM WITH SELECTED FIELDS"""
    def get_queryset(self):
        return self.get_queryset().filter().values("permission","role")


class RolesManager(models.Manager):
    """Returns Roles with Selected Fields"""
    def get_queryset(self):
        return self.filter().values_list('id', "name","guard_name")

class ModelHasPermissionsManager(models.Manager):
    """RETURNS MODELHASPERM WITH SELECTED FIELDS"""
    def get_queryset(self):
        return self.get_queryset().filter().values("permission","model_type", "model_id")

class ModelHasRoles(models.Manager):
    """RETURNS MODELHASROLES WITH SELECTED FIELDS"""
    def get_queryset(self):
        return self.get_queryset().filter().values_list("role","model_type","model_id")

class UserManager(models.Manager):
    """Returns active users with selected fields."""
    def active_users(self):
        return self.filter(is_active=True, deleted_at__isnull=True).values("name", "email", "password")

class UserUserManager(models.Manager):
    """Returns users under users"""
    def get_queryset(self):
        return self.get_queryset().values("id","parent","child")

class ScheduleUserManager(models.Manager):
    def get_queryset(self):
        return self.get_queryset().values("id", "user", "schedule")

############################################################################################################
"""SCHEDULES/ROOMS/SUBJECT/COURSES BELOW"""

class CourseManager(models.Manager):
    """Returns active courses with selected fields."""
    def active_courses(self):
        return self.filter(is_active=True, deleted_at__isnull=True).values("name", "code")

class SubjectManager(models.Manager):
    """Returns active subjects with selected fields."""
    def active_subjects(self):
        return self.filter(is_active=True, deleted_at__isnull=True).values("id","name", "code")


class RoomsManager(models.Manager):
    """Returns rooms with selected fields."""
    def active_rooms(self):
        return self.filter(is_active=True, deleted_at__isnull=True).values("id","name")

class ScheduleManager(models.Manager):
    """Returns active schedules with selected fields."""
    def active_schedules(self):
        return (self.select_related("course","professor","subject","room")
                .filter( )
                    .values("id", "course_id", "professor_id", "subject_id", "room_id",
                        "course__name","professor__name","subject__name","room__name",
                        "name", "time", "semester", "year", "is_active"))

"""EVALUATIONS(COPUS(STUDENT AND INSTRUCTOR).(EVALUATION FORM FOR INSTRUCTOR BY STUDENTS BELOW """
class StudentEvaluationManager(models.Manager):
    """Returns students eval with selected fields."""
    def student_evaluations(self):
        return self.select_related().filter().values("title", "description")



class StudentEvaluationsQuestions(models.Manager):
    """Returns students eval questions with selected fields."""
    def student_evaluations_questions(self):
        return self.filter().values("id", "student_evaluations_id", "question", "type", "options")

class StudentEvaluationsResponses(models.Manager):
    """Returns students eval responses with selected fields."""
    def student_evaluations_responses(self):
        return self.filter().values("id","student_evaluations_id","student_eval_question_id", "scheduled_id","year", "user_id", "answer")

class StudentEvaluationsSchedules(models.Manager):
    """Returns students eval schedules with selected fields."""
    def student_evaluations_schedules(self):
        return self.filter().values("id","scheduled_id","student_evaluations_id")


