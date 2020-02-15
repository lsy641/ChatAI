from django.db import models

class Uterrance(models.Model):
	text = models.CharField(max_length=200)
	speaker_idx = models.IntegerField()
	self_eval = models.IntegerField(default=5,null=True,blank=True)
	def __str__(self):
		return ""

class Hit(models.Model):
	hit_number = models.IntegerField(unique=True)
	security_code = models.CharField(max_length=10)
	worker1_name = models.CharField(max_length=50,null=True,blank=True)
	worker2_name = models.CharField(max_length=50,null=True,blank=True)
	current_conv = models.IntegerField(null=True,blank=True)
	def __str__(self):
		return ""

class Conversation(models.Model):
	hit = models.ForeignKey(Hit,on_delete=models.CASCADE)
	utterances = models.ManyToManyField(Uterrance,null=True,blank=True)
	scene = models.CharField(max_length=10)
	emotion = models.CharField(max_length=5)
	def __str__(self):
		return ""

