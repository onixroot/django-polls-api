from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
	'''Опрос'''
	question = models.CharField(max_length=100, verbose_name='Вопрос')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создано')
	pub_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question

	class Meta:
		verbose_name = 'Опрос'
		verbose_name_plural = 'Опросы'
		ordering = ['-pub_date']

class Choice(models.Model):
	poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=100)
	
	def __str__(self):
		return f"Проголосовало: {Vote.objects.filter(choice__exact=self.id).count()}"

	class Meta:
		verbose_name = 'Вариант'
		verbose_name_plural = 'Варианты'
		ordering = ['poll']

class Vote(models.Model):
	choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	voted_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Проголосовал')
	
	def __str__(self):
		return self.voted_by, self.poll, self.choice

	class Meta:
		unique_together = ("poll", "voted_by") #Sets of field names that, taken together, must be unique