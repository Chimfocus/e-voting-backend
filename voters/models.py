from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date, datetime
from usermanagement.models import User,Campus


class Election(models.Model):
    id = models.AutoField(primary_key=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default="Year Election")
    election_date = models.DateField()
    election_time = models.TimeField()
    active_election = models.BooleanField(default=False)

    def __str__(self):
        return f"Election {self.name} at {self.campus}"


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    candidate_position = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate_doc = models.FileField(upload_to='uploads/')
    candidate_description = models.TextField()

    def __str__(self):
        return f"Candidate {self.user.full_name} for {self.candidate_position}"


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    no_votes = models.IntegerField()
    votes_ranking = models.IntegerField()

    def __str__(self):
        return f"Vote by {self.user.full_name} for {self.candidate}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_description = models.TextField()

    def __str__(self):
        return f"Message {self.message_id} by {self.user.full_name}"
