from django import forms
from models import *


import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title

class TuneForm(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = Tune
        exclude = ('user','sheet_music')

class ConceptForm(forms.ModelForm):
    class Meta:
        model = Concept
        exclude = ('user')

class ResourceForm(forms.ModelForm):
    tune = MyModelChoiceField(queryset=Tune.objects.all(), empty_label="none",required=False)
    concept = MyModelChoiceField(queryset=Concept.objects.all(), empty_label="none",widget=forms.Select(),required=False)
    file = forms.FileField(required=False)
    class Meta:
        model = Resource
        exclude = ('user','file')


# Tables


import django_tables2 as tables
from django.utils.safestring import mark_safe

class ForeignFieldList(tables.Column):
    def render(self, value):
        output = ''
        for item in value.all():
            output += '<b>' + item.__unicode__() + ', </b>' 
        return mark_safe(output)

class ModifyColumn(tables.Column):
    def render(self, value, record):
        output = ' <a href="edit/'+str(record.id)+'">Edit</a>'
        output += ' <a href="remove/'+str(record.id)+'">Remove</a>'                
        return mark_safe(output)

class ClickableColumn(tables.Column):
    def render(self, value, record):
        return mark_safe('<a href="'+str(record.id)+'">'+value+'</a>')

class TuneTable(tables.Table):
    sheet_music = tables.URLColumn()    
    concepts = ForeignFieldList()
    id = ModifyColumn('Modify')
    title = ClickableColumn()
    class Meta:
        model = Tune
        exclude = ('user',)
        orderable = True
        sequence = ('date','...','id')
        
    def render_sheet_music(self,value):
        return mark_safe('<a href="'+value+'">View</a>')


class ConceptTable(tables.Table):
    tunes = ForeignFieldList()
    id = ModifyColumn('Modify')
    title = ClickableColumn()    
    class Meta:
        model = Concept
        exclude = ('user',)
        orderable = True
        sequence = ('...','id')

class ResourceTable(tables.Table):
    link = tables.URLColumn()
    file = tables.URLColumn()
    id = ModifyColumn('Modify')
    title = ClickableColumn()
    class Meta:
        model = Resource
        exclude = ('user',)
        orderable = True
        sequence = ('date','...','id')
    def render_file(self,value):
        return mark_safe('<a href="'+value+'">View</a>')
    def render_link(self,value):
        return mark_safe('<a href="'+value+'" target="_blank">View</a>')

