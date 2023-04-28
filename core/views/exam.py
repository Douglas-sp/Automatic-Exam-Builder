from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.models.exam import Exam


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exam.html'
    context_object_name = 'exams'
    login_url = reverse_lazy('login')
