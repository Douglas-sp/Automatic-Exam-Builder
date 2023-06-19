from django.views.generic import TemplateView
from django.urls import reverse_lazy
from core.models.answer import Answer
from core.models.question_bank import QuestionBank
from core.models.exam import Exam



class AnswerView(TemplateView):
    template_name = 'answer.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        exam_id = self.request.GET.get('exam_id')
        exam = Exam.objects.get(pk=exam_id)
        questions = QuestionBank.objects.filter(exam__id=exam_id)
        answers = Answer.objects.filter(question__exam__id=exam_id)
        question_answer_list = []

        for question in questions:
            answer = answers.filter(question=question).first()
            question_answer_list.append({
                'question': question.question_text,
                'answer': answer.answer_text if answer else 'No answer found'
            })

        context = super().get_context_data(**kwargs)
        context['question_answer_list'] = question_answer_list
        context['exam_name'] = exam.exam_name
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)