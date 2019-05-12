from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import jsonfield
import json
import numpy as np


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Create your models here.
class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    array = jsonfield.JSONField()
    arrayratedbooksindxs = jsonfield.JSONField()
    name = models.CharField(max_length=1000)
    lastrecs = jsonfield.JSONField()

    def __unicode__(self):
            return self.name

    def save(self, *args, **kwargs):
        create = kwargs.pop('create', None)
        recsvec = kwargs.pop('recsvec', None)

        if create==True:
             super(UserProfile, self).save(*args, **kwargs)
        elif recsvec!=None:
             self.lastrecs = json.dumps(recsvec.tolist())
             super(Userprofile, self).save(*args, **kwargs)
        else:
            nbooks = BookData.objects.count()
            array = np.zeros(nmovies)
            ratedmbooks = self.ratedbooks.all()
            self.arrayratedbooksindxs = json.dumps([m.bookindx for m in ratedbooks])

            for m in ratedbooks:
                array[m.bookindx] = m.value

            self.array = json.dumps(array.tolist())
            super(Userprofile, self).save(*args, **kwargs)


class BookRated(models.Model):
    user = models.ForeignKey(Userprofile, related_name='ratedbooks', on_delete=models.CASCADE)
    book = models.CharField(max_length=100)
    bookindx = models.IntegerField(default=-1)
    value = models.IntegerField()
    def __unicode__(self):
            return self.book


class BookData(models.Model):
    title = models.CharField(max_length=100)
    author = models.TextField()
    genre = models.TextField()
    info = models.TextField()
    keyword = models.TextField(default='책')
