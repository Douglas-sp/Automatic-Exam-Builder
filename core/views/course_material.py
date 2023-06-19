from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from core.engine.exam_gen import ExamGenerator
from core.models.course_material import CourseMaterial
from core.models.exam import Exam
from core.models.question_bank import QuestionBank
from core.models.answer import Answer
from core.utils.processor import DocumentProcessor

import threading


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

        document_processor = DocumentProcessor(course_material.course_file.path)
        document_processor.extract_text()
        processed_document = document_processor.process_text()

        exam_generator = ExamGenerator()
        exam_generator.add_documents(processed_document)

        # Create a thread for generating questions
        question_thread = threading.Thread(target=self.generate_questions_and_save, args=(exam, exam_generator))
        question_thread.start()

        # Add a success message
        messages.success(request, f'Exam generation for {course_material.course_name} in progress. Please wait.')

        return redirect('exam')

    def generate_questions_and_save(self, exam, exam_generator):
        questions = exam_generator.generate_questions()
        _questions = questions['questions']
        answers = questions['answers']
        print(len(questions))
        print(len(answers))

        question_objects = []
        answer_objects = []

        for question_text, answer_text in zip(_questions, answers):
            question = QuestionBank(exam=exam, question_text=question_text)
            question_objects.append(question)

            for _answer in answer_text:
                answer = Answer(answer_text=_answer.answer, question=question)
                answer_objects.append(answer)

        QuestionBank.objects.bulk_create(question_objects)
        Answer.objects.bulk_create(answer_objects)


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
