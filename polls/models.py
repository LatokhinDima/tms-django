from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Question(models.Model):
    class Status(models.TextChoices):
        NEW = 'NW', _('New')
        REJECTED = 'RJ', _('Rejected')
        APPROVED = 'AP', _('Approved')

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Publication date')
    status = models.CharField(max_length=2, choices=Status, default=Status.NEW)
    view_count = models.IntegerField(default=0)

    @admin.display(
        boolean=True,
        description='Published recently?',
        ordering='pub_date'
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text



class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='choices',
                                 on_delete=models.CASCADE)

    @admin.display(ordering='question__question_text', description='Question Text')
    def get_question_text(self):
        return self.question.question_text

    def __str__(self):
        return f'{self.question.question_text} - {self.choice_text}'


class User(models.Model):
    username = models.CharField(max_length=60)

    class Meta:
        abstract = True


class Guests(User):
    many_questions = models.IntegerField(default=0)


class RegisteredUsers(User):
    visit_date = models.DateTimeField('date of visit', db_index=True)

