from django.contrib import admin

from core.models.exam import Exam
from core.models.question_bank import QuestionBank
from core.models.user import User
from core.models.course_material import CourseMaterial

# Register your models here.
admin.site.register(User)
admin.site.register(CourseMaterial)
admin.site.register(Exam)
admin.site.register(QuestionBank)
