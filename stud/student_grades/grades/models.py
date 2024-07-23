from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - {self.subject}: {self.grade}'
