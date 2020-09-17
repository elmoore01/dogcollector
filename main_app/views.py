from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Dog Collector</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    return render(request, 'dogs/index.html', { 'dogs' : dogs })

class Dog:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

dogs = [
    Dog('McKenzie', 'Morkie', 'queen bee', 10),
    Dog('Taz', 'Mini Pin', 'the devil', 2),
    Dog('Coco', 'German Shepherd', 'the brains', 4),
    Dog('Apollo', 'German Shepherd', 'the braun', 4),
]