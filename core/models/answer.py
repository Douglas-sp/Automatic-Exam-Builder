from django.db import models
from core.models.timestamp import Timestamp


class Answer(Timestamp):
    answer_text = models.CharField(max_length=255, blank=False, null=False)
    question = models.ForeignKey('core.Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text