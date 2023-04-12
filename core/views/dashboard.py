from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy

from core.models.course_material import CourseMaterial
from core.models.exam import Exam
from core.models.question_bank import QuestionBank


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        course_materials = CourseMaterial.objects.all()
        exams = Exam.objects.all()
        question_banks = QuestionBank.objects.all()
        return render(request, 'dashboard.html',
                      {'course_materials': course_materials, 'exams': exams, 'question_banks': question_banks})
