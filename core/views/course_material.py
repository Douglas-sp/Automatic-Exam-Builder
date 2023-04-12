from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.models.course_material import CourseMaterial


class CourseMaterialListView(LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = 'course_material.html'
    context_object_name = 'course_materials'
    login_url = reverse_lazy('login')


class CourseMaterialCreateView(LoginRequiredMixin, CreateView):
    model = CourseMaterial
    fields = ('course_name', 'course_file')
    template_name = 'course_material_create.html'
    success_url = reverse_lazy('course_material')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
