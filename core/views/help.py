from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy

from core.models.course_material import CourseMaterial
from core.models.exam import Exam
from core.models.question_bank import QuestionBank
from core.models import User


class DashboardView(LoginRequiredMixin, View):
    """
    View to display the dashboard.

    Inherits from LoginRequiredMixin and View.
    """
    login_url = reverse_lazy('login')

    def get(self, request):
        """
        Handle GET request to retrieve dashboard data.

        Retrieves the counts of course materials, exams, question banks, and users from the database.
        Creates a context dictionary with the analytics data.
        Renders the dashboard.html template with the context.
        """
        course_materials = CourseMaterial.objects.count()
        exams = Exam.objects.count()
        question_banks = QuestionBank.objects.count()
        users = User.objects.count()
        context = {}
        context['analytics'] = [{'course_materials': course_materials, 'exams': exams, 'question_banks': question_banks, 'users': users}]
        return render(request, 'dashboard.html', context)

    def helpView(request):
        return render(request, 'help.html')
