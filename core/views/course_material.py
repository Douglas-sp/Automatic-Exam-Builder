from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.models.course_material import CourseMaterial
from core.models.exam import Exam
from core.models.question_bank import QuestionBank
from core.engine.exam_gen import ExamGenerator
from core.engine.exam_gen_v2 import ExamGenerationModule


class CourseMaterialListView(LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = 'course_material.html'
    context_object_name = 'course_materials'
    login_url = reverse_lazy('login')


class CourseMaterialCreateView(LoginRequiredMixin, CreateView):
    model = CourseMaterial
    fields = ('course_name', 'course_file')
    template_name = 'course_material_create.html'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        course_material = CourseMaterial.objects.create(
            course_name=request.POST['course_name'],
            course_file=request.FILES['course_file']
        )
        exam_generator = ExamGenerator(course_material.course_file.read().decode('utf-8'))

        exam_generator.analyze_course_material()
        exam_generator.generate_questions()
        exam_generator.filter_questions()

        questions = exam_generator.get_questions()
        print(exam_generator.format_exam())

        exam = Exam.objects.create(
            exam_name=course_material.course_name,
            description=f"Exam for {course_material.course_name}",
        )

        for question in questions:
            QuestionBank.objects.create(
                exam=exam,
                question_text=question['text'],
            )

        return redirect('exam')


class CourseMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = CourseMaterial
    fields = ('course_name', 'course_file')
    template_name = 'course_material_update.html'
    success_url = reverse_lazy('course_material')
    login_url = reverse_lazy('login')


class CourseMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = CourseMaterial
    template_name = 'course_material_delete.html'
    success_url = reverse_lazy('course_material')
    login_url = reverse_lazy('login')


class CourseMaterialV2CreateView(LoginRequiredMixin, CreateView):
    model = CourseMaterial
    fields = ('course_name', 'course_file')
    template_name = 'course_material_v2_create.html'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        course_material = CourseMaterial.objects.create(
            course_name=request.POST['course_name'],
            course_file=request.FILES['course_file']
        )

        exam_generator = ExamGenerationModule([course_material.course_file.read().decode('utf-8')])
        questions = exam_generator.generate_exam()

        print(questions)

        exam = Exam.objects.create(
            exam_name=course_material.course_name,
            description=f"Exam for {course_material.course_name}",
        )

        for question in questions:
            QuestionBank.objects.create(
                exam=exam,
                question_text=question,
            )

        return redirect('exam')