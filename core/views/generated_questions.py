from django.views.generic import TemplateView
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from core.models.question_bank import QuestionBank
from django.urls import reverse_lazy


class GeneratedQuestionsView(TemplateView):
    template_name = 'generated_questions.html'
    login_url = reverse_lazy('login')

    def generate_pdf(self, question_list):
        buffer = BytesIO()

        # Create the PDF object, using the buffer as its "file".
        p = canvas.Canvas(buffer, pagesize='A4')

        # Set up the PDF content.
        p.setFont("Helvetica", 12)
        p.drawString(30, 780, "Generated Questions")

        y = 750
        question_number = 1
        for question in question_list:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(30, y, f"Question {question_number}: {question.question_text}")
            p.setFont("Helvetica", 10)
            p.drawString(30, y - 20, f"Exam: {question.exam.exam_name}")
            y -= 40
            question_number += 1
            if y <= 70:
                p.showPage()
                y = 750

        p.save()

        # Get the value of the BytesIO buffer and return the response as PDF.
        pdf_value = buffer.getvalue()
        buffer.close()
        return pdf_value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.request.GET.get('exam_id')
        if exam_id:
            questions = QuestionBank.objects.filter(exam__id=exam_id)
        else:
            questions = QuestionBank.objects.all()
        context['question_list'] = questions
        context['current_date'] = timezone.now().date()
        context['exam_id'] = exam_id
        return context

    def post(self, request, *args, **kwargs):
        exam_id = request.POST.get('exam_id')
        if exam_id:
            questions = QuestionBank.objects.filter(exam__id=exam_id)
        else:
            questions = QuestionBank.objects.all()

        pdf_value = self.generate_pdf(questions)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="generated_questions.pdf"'

        # Write the PDF value as the response content.
        response.write(pdf_value)

        return response
