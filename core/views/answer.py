from django.views.generic import TemplateView
from django.urls import reverse_lazy
from core.models.answer import Answer


class AnswerView(TemplateView):
    template_name = 'answer.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        exam_id = self.kwargs['exam_id']
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question__exam__id=exam_id)
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)