from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TaskStatus(models.Model):
    status = models.CharField(max_length=32, unique=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, related_name='task_status')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-created_at']

    def __str__(self):
        return self.title
