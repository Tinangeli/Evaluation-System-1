"""REFER TO CUSTOMMODELS FOR EDITING VIEW OF DATA"""
from django.db import models

from hrapp.models.CustomModels import *
from django.utils import timezone
from hrapp.models import CustomModels
#IMPORTANT! READ THE DESCRIPTION BELOW TO UNDERSTAND THE RELATIONSHIP OF TABLES AND INFORMATION TO EACH

#USERS TABLE AND OTHER RELATION
"""users: Stores user details (name, email, password).
roles: Defines different roles (e.g., admin, professor, student).
permissions: Stores actions users can perform.
model_has_roles: Associates roles with users.
model_has_permissions: Associates permissions with users.
role_has_permissions: Links roles to permissions."""
#A user can have multiple roles, and roles define permissions. Permissions can also be directly assigned to users.

#PROFESSOR DEAN RELATION
"""dean_professor: Links deans and professors.
dean_id → References users.id (dean).
professor_id → References users.id (professor).
"""
#Summary: A professor can be supervised by a dean.

#SCHEDULE: ROOMS, COURSE, SUBJECTS. RELATIONS
"""courses: Stores course details.
subjects: Stores subjects taught in courses.
rooms: Stores classroom details.
schedules: Defines class schedules 
    Links to courses, users (professors), subjects, and rooms."""
#Summary: A schedule ties a course, subject, professor, and room to a specific time and semester.

#TEACHING LOAD RELATION
"""teaching_load: Assigns schedules to professors.
 Summary: Each professor has a defined teaching load based on assigned schedules."""

#COPUS EVALUATION RELATION
"""evaluation: Tracks evaluations for instructors/students.
Links to instructor_categories, student_categories, evaluation_marks, users (evaluator), schedules, and evaluation_comments.
student_categories and instructor_categories: Stores evaluation criteria.
evaluation_marks: Stores evaluation scores.
evaluation_comments: Stores comments on evaluations."""
# Summary: The evaluation system assesses instructors and students, records scores, and allows comments.


# Create your models here.



#  Cache Manager


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cache(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expiration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cache'


class CacheLocks(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    owner = models.CharField(max_length=255)
    expiration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cache_locks'


class Courses(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    is_active = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = CourseManager()

    class Meta:
        managed = False
        db_table = 'courses'

    def __str__(self):
        return f" {self.id} ,{self.name} |  | Code: {self.code}"

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Evaluations(models.Model):
    id = models.BigAutoField(primary_key=True)
    dean = models.ForeignKey('Users', models.DO_NOTHING)
    schedule = models.ForeignKey('Schedules', models.DO_NOTHING)
    observation_date = models.DateField()
    evaluation_type = models.CharField(max_length=255)
    additional_comments = models.TextField(blank=True, null=True)
    student_activities = models.JSONField(blank=True, null=True)
    instructor_activities = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluations'

    def __str__(self):
        return f"{self.id} | {self.dean} | {self.schedule} | {self.observation_date} | {self.evaluation_type} | {self.additional_comments} | {self.student_activities} | {self.instructor_activities}"

class Exports(models.Model):
    id = models.BigAutoField(primary_key=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    file_disk = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    exporter = models.CharField(max_length=255)
    processed_rows = models.PositiveIntegerField()
    total_rows = models.PositiveIntegerField()
    successful_rows = models.PositiveIntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exports'

    def __str__(self):
        return f"{self.id} | {self.completed_at} | {self.file_disk} | {self.file_name} | {self.exporter} | {self.processed_rows} | {self.total_rows} | {self.successful_rows} | {self.user}"

    

class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'

class Imports(models.Model):
    id = models.BigAutoField(primary_key=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    importer = models.CharField(max_length=255)
    processed_rows = models.PositiveIntegerField()
    total_rows = models.PositiveIntegerField()
    successful_rows = models.PositiveIntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imports'

    def __str__(self):
        return f"{self.id} | {self.completed_at} | {self.file_name} | {self.file_path} | {self.importer} | {self.processed_rows} | {self.total_rows} | {self.successful_rows} | {self.user}"

class JobBatches(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    total_jobs = models.IntegerField()
    pending_jobs = models.IntegerField()
    failed_jobs = models.IntegerField()
    failed_job_ids = models.TextField()
    options = models.TextField(blank=True, null=True)
    cancelled_at = models.IntegerField(blank=True, null=True)
    created_at = models.IntegerField()
    finished_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_batches'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=255)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'jobs'

    def __str__(self):
        return f"{self.id}, {self.queue}, {self.payload}, {self.attempts}, {self.reserved_at}, {self.available_at}"

class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class ModelHasPermissions(models.Model):
    permission = models.OneToOneField('Permissions', models.DO_NOTHING, primary_key=True)  # The composite primary key (permission_id, model_id, model_type) found, that is not supported. The first column is selected.
    model_type = models.CharField(max_length=255)
    model_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_has_permissions'
        unique_together = (('permission', 'model_id', 'model_type'),)


class ModelHasRoles(models.Model):
    role = models.OneToOneField('Roles', models.DO_NOTHING, primary_key=True)  # The composite primary key (role_id, model_id, model_type) found, that is not supported. The first column is selected.
    model_type = models.CharField(max_length=255)
    model_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_has_roles'
        unique_together = (('role', 'model_id', 'model_type'),)


class Notifications(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=255)
    notifiable_type = models.CharField(max_length=255)
    notifiable_id = models.PositiveBigIntegerField()
    data = models.TextField()
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'

    def __str__(self):
        return f"{self.id} | {self.type} | {self.notifiable_type} | {self.notifiable_id} | {self.data} | {self.read_at} | {self.created_at} | {self.updated_at}"

class PasswordResetTokens(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_reset_tokens'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    guard_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'
        unique_together = (('name', 'guard_name'),)

    def __str__(self):
        return f"{self.id} {self.name} | {self.guard_name}"


class RoleHasPermissions(models.Model):
    permission = models.OneToOneField(Permissions, models.DO_NOTHING, primary_key=True)  # The composite primary key (permission_id, role_id) found, that is not supported. The first column is selected.
    role = models.ForeignKey('Roles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role_has_permissions'
        unique_together = (('permission', 'role'),)


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    guard_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
        unique_together = (('name', 'guard_name'),)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.guard_name}"

class Rooms(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'

    def __str__(self):
        return f"{self.id} | {self.name} |  {self.is_active}"


class ScheduleUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    schedule = models.ForeignKey('Schedules', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_user'

    def __str__(self):
        return f"{self.id} | {self.user} | {self.schedule}"


class Schedules(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    professor = models.ForeignKey('Users', models.DO_NOTHING)
    subject = models.ForeignKey('Subjects', models.DO_NOTHING)
    room = models.ForeignKey(Rooms, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    time = models.TimeField()
    semester = models.CharField(max_length=255)
    year = models.TextField()  # This field type is a guess.
    is_active = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now())
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = ScheduleManager()

    class Meta:
        managed = False
        db_table = 'schedules'

    def __str__(self):
        return f"ID: {self.id} Course: {self.course} Prof: {self.professor} Sub: {self.subject} Room: {self.room} Name: {self.name} Time: {self.time} Sem: {self.semester} Yr: {self.year}"




class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'


class StudentEvaluationQuestions(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_evaluation = models.ForeignKey('StudentEvaluations', models.DO_NOTHING)
    question = models.TextField()
    type = models.CharField(max_length=15)
    options = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_evaluation_questions'

    def __str__(self):
        return f"{self.id} | {self.student_evaluation} | {self.question}, {self.type}, {self.options}"


class StudentEvaluationResponses(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_evaluation = models.ForeignKey('StudentEvaluations', models.DO_NOTHING)
    student_eval_question = models.ForeignKey(StudentEvaluationQuestions, models.DO_NOTHING)
    schedule = models.ForeignKey(Schedules, models.DO_NOTHING)
    year = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    answer = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_evaluation_responses'

    def __str__(self):
        return f"{self.id}, {self.student_evaluation}, {self.student_evaluation}, {self.schedule}, {self.year}, {self.user}, {self.answer}, {self.created_at}, {self.updated_at}"


class StudentEvaluationSchedules(models.Model):
    id = models.BigAutoField(primary_key=True)
    schedule = models.ForeignKey(Schedules, models.DO_NOTHING)
    student_evaluation = models.ForeignKey('StudentEvaluations', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_evaluation_schedules'

    def __str__(self):
        return f"{self.id} | {self.schedule} | {self.student_evaluation}"


class StudentEvaluations(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_evaluations'

    def __str__(self):
        return f"{self.id} | {self.title} , {self.description} , {self.is_active}"

class Subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'

    def __str__(self):
        return f"{self.id} | {self.name} | {self.is_active}"


class UserUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent = models.ForeignKey('Users', models.DO_NOTHING)
    child = models.ForeignKey('Users', models.DO_NOTHING, related_name='useruser_child_set')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_user'

    def __str__(self):
        return f"{self.id} | {self.parent} | {self.child}"


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    parent_id = models.PositiveBigIntegerField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


    def __str__(self):
        return f"{self.id} | {self.name}, {self.email}, {self.email_verified_at}, {self.password}, {self.created_at}, {self.updated_at}"
