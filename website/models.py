from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('Todo', 'Todo'),
        ('Inprogress', 'Inprogress'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Todo')
    members = models.ManyToManyField(User, related_name='tasks')

    def __str__(self):
        return self.title