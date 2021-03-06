from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from status.models import Status
from django.contrib.auth.models import User

from django.db import models
import datetime
from django.utils import timezone

class Project(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField()
	dead_line = models.DateField()
	create_date = models.DateField(default = datetime.date.today)
	slug = models.CharField(max_length=50, default="")

	def validate_unique(self, exclude=None):
		self.slug = self.create_slug_field(self.title)
		if Project.objects.filter(slug = self.slug).exclude(pk = self.id).exists():
			raise ValidationError('Un proyecto con el mismo titulo ya se encuentra registrado.')

	def create_slug_field(self, value):
		return value.lower().replace(" ", "-")

	def get_id_status(self):
		return self.projectstatus_set.last().status_id

	def get_status(self):
		return self.projectstatus_set.last().status

	def __str__(self):
		return self.title

class ProjectStatus(models.Model):
	project = models.ForeignKey(Project)
	status = models.ForeignKey(Status)
	create_date = models.DateTimeField(default = timezone.now)

class ProjectPermission(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField()
	level = models.IntegerField()
	create_date = models.DateTimeField(default = timezone.now)

class ProjectUser(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE)
	user = models.ForeignKey(User)
	permission = models.ForeignKey(ProjectPermission)
	create_date = models.DateTimeField(default = timezone.now)

	def get_project(self):
		return self.project


