from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

'''
music: user, id, type(like/dislike)
user:username ,pw
'''


class Music(models.Model):
    user = models.ForeignKey(User)
    music_id = models.IntegerField()
    type = models.BooleanField(default=True)  # True like /  False dislike

    def __unicode__(self):
        return self.user.username + '-' + str(self.music_id) + '-' + str(self.type)


# class ExtUser(models.Model):
#     user = models.OneToOneField(User)
#     number = models.IntegerField(primary_key=True)
#     sex = models.CharField(max_length=2, blank=True, null=True)
#     autograph = models.CharField(max_length=50, blank=True, null=True)
#     greet = models.CharField(max_length=50, blank=True, null=True)
#     labels = models.CharField(max_length=50, blank=True, null=True)
#     register_date = models.DateField(auto_now=True)
#
#     def __unicode__(self):
#         return self.user.username