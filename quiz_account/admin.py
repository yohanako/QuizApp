from django.contrib import admin
from .models import Question, Teacher, Student, Result, Course

#admin.site.register(Questions)
admin.site.register(Question)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Course)