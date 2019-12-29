from django.db import models


class Task(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PRIORITY_CHOICES = ((LOW, 'Low'), (MEDIUM, 'Medium'), (HIGH, 'High'))

    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<task: {self.title}>'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('todos:task-detail', args=[int(self.id)])

    class Meta:
        ordering = ('-priority',)
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

#
# class Reminder(models.Model):
#     task = models.ForeignKey('Task', related_name='reminders_ids', on_delete=models.CASCADE)
#     date = models.DateTimeField(blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'<reminder: {self.date}>'
#
#     class Meta:
#         ordering = ('-date',)
#         verbose_name = 'reminder'
#         verbose_name_plural = 'reminders'
#
#
# class Comment(models.Model):
#     task = models.ForeignKey('Task', related_name='comments_ids', on_delete=models.CASCADE)
#     comment = models.CharField(max_length=500, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'<comment: {self.comment}>'
#
#     class Meta:
#         ordering = ('-created_at',)
#         verbose_name = 'comment'
#         verbose_name_plural = 'comments'
