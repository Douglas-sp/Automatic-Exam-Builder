from django.db import models
from core.models.timestamp import Timestamp


class Exam(Timestamp):
    exam_name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.exam_name
