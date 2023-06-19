from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from core.models.exam import Exam


class ExamListView(ListView):
    model = Exam
    template_name = 'exam.html'
    context_object_name = 'exams'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')  # Modify the ordering as per your requirement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Get the complete queryset
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        exams = paginator.get_page(page_number)
        context[self.context_object_name] = exams
        return context

