from django.db import models
from datetime import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Tags(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    