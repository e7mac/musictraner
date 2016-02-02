from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from django.conf import settings
from forms import *
from models import *
import os

from django_tables2 import RequestConfig

from boto.s3.connection import S3Connection
from boto.s3.key import Key


TMP_DIR = '/tmp/'

#Tunes

@login_required
def list_tunes(request):
    tunes = Tune.objects.filter(user=request.user).order_by('-date')
    table = TuneTable(tunes)
    RequestConfig(request).configure(table)
    return render_to_response('tunes/list.html', {'table': table, 'section':'Tune'},
                              context_instance=RequestContext(request))
@login_required
def add_tune(request):
    if request.method == 'POST':
        form = TuneForm(request.POST, request.FILES)
        if form.is_valid():
            #try uploading, skip if not found
            try:
                tune = form.save()
                tune.user = request.user
                tune.save()
                try:
                    upload_sheet_music(tune, request.FILES['file'],request.user.username)
                except Exception:
                    pass
                return HttpResponseRedirect(reverse('tunes-list', args=[request.user.username]))
            except Exception:
                return HttpResponse("error in saving")
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        form = TuneForm()
        variables = RequestContext(request, {'form':form, 'section':'Tune'})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')


@login_required
def edit_tune(request,id):
    if request.method == 'POST':
        item = Tune.objects.get(id=id)
        item.delete()
        form = TuneForm(request.POST, request.FILES)
        if form.is_valid():
            #try uploading, skip if not found
            try:
                tune = form.save()
                tune.user = request.user
                tune.save()
                try:
                    upload_sheet_music(tune, request.FILES['file'],request.user.username)
                    delete_file(item.sheet_music)
                except Exception:
                    tune.sheet_music = item.sheet_music
                    tune.save()
                return HttpResponseRedirect(reverse('tunes-list', args=[request.user.username]))
            except Exception:
                return HttpResponse(item.file)
                variables = RequestContext(request, {'form':form, 'section':'Tune'})
                return render_to_response('tunes/add.html',variables)
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        item = Tune.objects.get(id=id)
        form = TuneForm(instance=item)
        variables = RequestContext(request, {'form':form, 'section':'Tune'})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')

@login_required
def show_tune(request,id):
    tune = Tune.objects.get(id=id)
    type='none'
    if tune.sheet_music:
        type = tune.sheet_music.rpartition('.')[2]
        if type=='jpg' or type=='jpeg' or type=='png' or type=='gif':
            type = 'img'
    return render_to_response('tunes/show_tune.html',{'tune':tune,'type':type,'section':'Tune'},context_instance=RequestContext(request))

@login_required
def remove_tune(request,id):
    tune = Tune.objects.get(id=id)
    tune.delete()
    try:
        delete_file(tune.sheet_music)
    except Exception:
        pass
    return HttpResponseRedirect(reverse('tunes-list', args=[request.user.username]))


#Concepts

@login_required
def list_concepts(request):
    concepts = Concept.objects.filter(user=request.user)
    table = ConceptTable(concepts)
    RequestConfig(request).configure(table)
    return render_to_response('tunes/list.html', {'table': table, 'section':'Concept'},
                              context_instance=RequestContext(request))
@login_required
def add_concept(request):
    if request.method == 'POST':
        form = ConceptForm(request.POST)
        if form.is_valid():
            concept = form.save()
            concept.user = request.user
            concept.save()
            return HttpResponseRedirect(reverse('concepts-list', args=[request.user.username]))
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        form = ConceptForm()
        variables = RequestContext(request, {'form':form, 'section':'Concept'})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')

@login_required
def edit_concept(request,id):
    if request.method == 'POST':
        item = Concept.objects.get(id=id)
        item.delete()
        form = ConceptForm(request.POST)
        if form.is_valid():
            concept = form.save()
            concept.user = request.user
            concept.save()
            return HttpResponseRedirect(reverse('concepts-list', args=[request.user.username]))
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        item = Concept.objects.get(id=id)
        form = ConceptForm(instance=item)
        variables = RequestContext(request, {'form':form, 'section':'Concept'})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')

@login_required
def show_concept(request,id):
    concept = Concept.objects.get(id=id)
    return render_to_response('tunes/show_concept.html',{'concept':concept,'section':'Concept'},context_instance=RequestContext(request))

@login_required
def remove_concept(request,id):
    concept = Concept.objects.get(id=id)
    concept.delete()
    return HttpResponseRedirect(reverse('concepts-list', args=[request.user.username]))


#Resources

@login_required
def list_resources(request):
    resources = Resource.objects.filter(user=request.user)
    table = ResourceTable(resources)
    RequestConfig(request).configure(table)
    return render_to_response('tunes/list.html', {'table': table, 'section':'Resource',},
                              context_instance=RequestContext(request))
@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = form.save()
                resource.user = request.user
                resource.save()
                try:
                    file = request.FILES['file']
                    upload_resource(resource,file,request.user.username)
                except Exception:
                    pass
                return HttpResponseRedirect(reverse('resources-list', args=[request.user.username]))
            except Exception:
                return HttpResponse("error in saving form")
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        form = ResourceForm()
        variables = RequestContext(request, {'form':form, 'section':'Resource',})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')

@login_required
def edit_resource(request,id):
    if request.method == 'POST':
        item = Resource.objects.get(id=id)
        item.delete()
        form = ResourceForm(request.POST)
        if form.is_valid():
            try:
                resource = form.save()
                resource.user = request.user
                resource.save()
                try:
                    file = request.FILES['file']
                    upload_resource(resource,file,request.user.username)
                    delete_file(item.file)
                except Exception:
                    resource.file = item.file
                    resource.save()
                return HttpResponseRedirect(reverse('resources-list', args=[request.user.username]))
            except Exception:
                return HttpResponse("error in saving form")
        else:
            return HttpResponse("Error in:" + str(form.errors))
    else:
        item = Resource.objects.get(id=id)
        form = ResourceForm(instance=item)
        variables = RequestContext(request, {'form':form, 'section':'Resource',})
        return render_to_response('tunes/add.html',variables)
    return HttpResponse('form logic error')

@login_required
def show_resource(request,id):
    resource = Resource.objects.get(id=id)
    type='none'
    if resource.file:
        type = resource.file.rpartition('.')[2]
        if type=='jpg' or type=='jpeg' or type=='png' or type=='gif':
            type = 'img'
    return render_to_response('tunes/show_resource.html',{'resource':resource,'type':type,'section':'Resource', },context_instance=RequestContext(request))


@login_required
def remove_resource(request,id):
    resource = Resource.objects.get(id=id)
    resource.delete()
    try:
        delete_file(resource.file)
    except Exception:
        pass
    return HttpResponseRedirect(reverse('resources-list', args=[request.user.username]))



# Upload Functions

def upload_resource(resource,file,username):
    target_dir = TMP_DIR + username + '/resources/'
    try:
        os.makedirs(target_dir)
    except Exception:
        pass
    upload_file(target_dir,file.name,file)
    resource.file = settings.MEDIA_URL+ username +'/resources/' + file.name
    resource.save()

def upload_sheet_music(tune, file,username):
    target_dir = TMP_DIR + username + '/'+tune.artist
    try:
        os.makedirs(target_dir)
    except Exception:
        pass
    target_file = tune.title + '.' + file.name.rpartition('.')[2]
    upload_file(target_dir,target_file,file)
    tune.sheet_music = settings.MEDIA_URL+ username + '/' + tune.artist + '/' + target_file
    tune.save()

def upload_file(target,filename,file):
    with open(target+'/'+filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    UploadMediaFileToS3(target+'/'+filename)
    os.remove(target+'/'+filename)

def UploadMediaFileToS3(filePath):
    awskey = ''
    awssecret = ''
    conn = S3Connection(awskey, awssecret)
    bucket = conn.get_bucket('musictraner-media.e7mac.com')
    k = Key(bucket)
    k.key = filePath.rsplit(TMP_DIR)[1]
    k.set_contents_from_filename(filePath)


# Convenience OS functions



def url_to_filepath(url):
    unique_path = url.rpartition(settings.MEDIA_URL)[2]
    filepath = TMP_DIR + unique_path
    return filepath

def filepath_to_url(filepath):
    unique_path = filepath.rpartition(TMP_DIR)[2]
    url = settings.MEDIA_URL + unique_path
    return url

def delete_file(url):
    filepath = url_to_filepath(url)
    try:
        os.remove(filepath)
    except:
        pass


# User Account Views

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            )
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if new_user is not None:
                if new_user.is_active:
                    login(request, new_user)
                return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'form':form})
            return render_to_response('registration/register.html',variables)
    else:
        form = UserCreationForm()
        variables = RequestContext(request, {'form':form, 'section':'Register'})
        return render_to_response('registration/register.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def main_page(request):
    variables = RequestContext(request, {'section':'Home'})
    return render_to_response('home.html',variables)

def contact(request):
    variables = RequestContext(request, {'section':'Contact'})
    return render_to_response('contact.html',variables)

def links(request):
    variables = RequestContext(request, {'section':'Links'})
    return render_to_response('links.html',variables)


# User cloning function
from string import replace
from shutil import copyfile

def clone_user(new_user,user):
    concepts = Concept.objects.filter(user=user)
    tunes = Tune.objects.filter(user=user)
    resources = Resource.objects.filter(user=user)
    for item in concepts:
        item.pk = None
        item.user = new_user
        item.save()
    for item in tunes:
        item.pk = None
        item.user = new_user
        old_file = item.sheet_music
        item.sheet_music=replace(item.sheet_music,user.username,new_user.username)
        try:
            os.makedirs(url_to_filepath(item.sheet_music).rpartition('/')[0])
        except:
            pass
        copyfile(url_to_filepath(old_file),url_to_filepath(item.sheet_music))
        item.save()
    for item in resources:
        item.pk = None
        item.user = new_user
        try:
            old_file = item.file
            item.file= replace(item.file,user.username,new_user.username)
            os.makedirs(url_to_filepath(item.file).rpartition('/')[0])
            copyfile(url_to_filepath(old_file),url_to_filepath(item.file))
        except:
            pass
        item.save()

def delete_user_db(username):
    user = User.objects.get(username=username)
    concepts = Concept.objects.filter(user=user)
    tunes = Tune.objects.filter(user=user)
    resources = Resource.objects.filter(user=user)
    for item in concepts:
        item.delete()
    for item in tunes:
        item.delete()
    for item in resources:
        item.delete()
