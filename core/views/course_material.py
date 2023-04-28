from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.engine.exam_gen import ExamGenerator
from core.models.course_material import CourseMaterial
from core.models.exam import Exam
from core.models.question_bank import QuestionBank
from core.utils.processor import DocumentProcessor


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

        exam = Exam.objects.create(
            exam_name=course_material.course_name,
            description=f"Exam for {course_material.course_name}",
        )

        document_processor = DocumentProcessor(course_material.course_file)
        document_processor.extract_text()
        processed_document = document_processor.process_text()

        exam_generator = ExamGenerator()

        exam_generator.add_documents(processed_document)

        exam_generator.generate_questions()

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

        exam = Exam.objects.create(
            exam_name=course_material.course_name,
            description=f"Exam for {course_material.course_name}",
        )

        return redirect('exam')
