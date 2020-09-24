import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dog, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-sei-9-elm'

# Create your views here.

from django.http import HttpResponse

class DogCreate(CreateView):
    model = Dog
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/dogs/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DogUpdate(UpdateView):
    model = Dog
    fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

def home(request):
    return HttpResponse('<h1>Dog Collector</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', { 'dogs' : dogs })

def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    # Get the toys the dog doesn't have
    toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', { 
        'dog': dog, 'feeding_form': feeding_form,
        # Add the toys to be displayed
        'toys': toys_dog_doesnt_have
    })

def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the dog_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

def assoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)

def unassoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def add_photo(request, dog_id):
  # photo-file will be the "name" attribute on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" / but keep the file extension (image type)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case we get an error
    try:
        
      print(photo_file) 
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      Photo.objects.create(url=url, dog_id=dog_id)
    except:
      print('An error occured uploading file to S3')
  return redirect('detail', dog_id=dog_id)
