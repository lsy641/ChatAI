from django.db import models

class Utterance(models.Model):
	text = models.CharField(max_length=200)
	speaker_idx = models.IntegerField()
	send_time = models.DateTimeField(auto_now=True)
	self_eval = models.IntegerField(default=5,null=True,blank=True)
	def __str__(self):
		return ""

class Hit(models.Model):
	hit_number = models.IntegerField(unique=True)
	security_code = models.CharField(max_length=10)
	speaker_name = models.CharField(max_length=50,null=True,blank=True)
	listener_name = models.CharField(max_length=50,null=True,blank=True)
	hit_state = models.IntegerField(default=0)
	current_conv = models.IntegerField(null=True,blank=True)
	def __str__(self):
		return ""

class Conversation(models.Model):
	hit = models.ForeignKey(Hit,on_delete=models.CASCADE,null=True,blank=True)
	utterances = models.ManyToManyField(Utterance)
	scene = models.CharField(max_length=10)
	emotion = models.CharField(max_length=5)
	context = models.CharField(max_length=200,null=True,blank=True)

	def __str__(self):
		return ""

