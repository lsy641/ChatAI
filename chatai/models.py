from django.db import models

# Create your models here.

class Hit(models.Model):
	security_code = models.IntegerField()
	worker1_name = models.CharField(max_length=50)
	worker2_name = models.CharField(max_length=50)
	current_conv = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	def __str__(self):
		return ""

class Uterrance(models.Model):
	text = models.CharField(max_length=200)
	speaker_idx = models.IntegerField()
	self_eval = models.IntegerField(default=5)
	def __str__(self):
		return ""

class Conversation(models.Model):
	hit = models.ForeignKey(Hit,on_delete=models.CASCADE)
	utterances = models.OneToOneField(Hit, on_delete=models.CASCADE, primary_key=True)
	def __str__(self):
		return ""
	
