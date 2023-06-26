from django.db import models

from django.contrib.auth.models import User

STATUS_CHOICES = [
    ["PENDING", "Pending"],
    ["IN_PROGRESS", "In Progress"],
    ["COMPLETED", "Completed"],
    ["CANCELLED", "Cancelled"],
]


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title


STATUS_CHOICES_HISTORY = [
    ["CREATED", "Created"],
] + STATUS_CHOICES


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    old_status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES_HISTORY,
        default=STATUS_CHOICES_HISTORY[0][0],
    )
    new_status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES_HISTORY,
        default=STATUS_CHOICES_HISTORY[1][0],
    )
    changed_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
