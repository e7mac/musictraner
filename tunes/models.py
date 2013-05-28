from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.

class Concept(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024,blank=True,null=True)
    tunes = models.ManyToManyField('Tune',blank=True,null=True)
    
    def __unicode__(self):
        return mark_safe("<a href=\"/"+self.user.username+"/concepts/"+str(self.id)+"/\">"+self.title+"</a>")

class Tune(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    title = models.CharField(max_length=512)
    artist = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    key = models.CharField(max_length=16,blank=True,null=True)
    genre = models.CharField(max_length=16,blank=True,null=True)
    tempo = models.IntegerField(blank=True,null=True)
    sheet_music = models.URLField(blank=True,null=True)
    concepts = models.ManyToManyField(Concept,blank=True,null=True,through=Concept.tunes.through)
    
    def __unicode__(self):
        return mark_safe("<a href=\"/"+self.user.username+"/tunes/"+str(self.id)+"/\">"+self.title+"</a>")

class Resource(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    title = models.CharField(max_length=128,blank=True,null=True)
    notes = models.CharField(max_length=10240,blank=True,null=True)
    tune = models.ForeignKey(Tune,blank=True,null=True)
    concept = models.ForeignKey(Concept,blank=True,null=True)
    file = models.URLField(blank=True,null=True)
    link = models.URLField(blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    
    def __unicode__(self):
        return mark_safe("<a href=\"/"+self.user.username+"/resources/"+str(self.id)+"/\">"+self.title+"</a>")
