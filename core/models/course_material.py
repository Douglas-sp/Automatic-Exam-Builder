from django.db import models
from core.models.timestamp import Timestamp


class CourseMaterial(Timestamp):
    course_name = models.CharField(max_length=255, blank=False, null=False)
    upload_date = models.DateField(auto_now_add=True)
    course_file = models.FileField(upload_to='course_materials', blank=False, null=False)

    def __str__(self):
        return self.course_name
