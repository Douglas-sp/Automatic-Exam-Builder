from django.db import models
from core.models.timestamp import Timestamp


class QuestionBank(Timestamp):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.question_text

    @property
    def exam_name(self):
        return self.exam.exam_name
