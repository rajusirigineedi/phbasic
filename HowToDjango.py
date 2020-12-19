# Create a virtual env in a folder
python -m virtualenv envname  (or)  pyhton -m virtualenv . (to make the same folder as virtualenv)

# Go to env folder and activate
.\Scripts\activate (to activate)
deactivate  (to deactivate)

# Next go to parent folder and create a django project there.. If django not installed in env install it
pip install django

# create a project
django-admin startproject projectname

# after this modify the projectname folder as different one to avoid conflicts while reading
rename > projectname > projectname-project

# go into settings and copy some static and media root and urls
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Go to project level urls.py and add these static workers
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#To run server
python manage.py runserver

# Create a app
python manage.py startapp appname

# initialize the new apps in settings.py`
INSTALLED_APPS = [
    'appname',
]

# create urls.py file in apps
create > urls.py

#copy content to app's urls.py
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
]


# include app urls in project urls
from django.urls import path, include
import account.urls
[
    path('account/', include(account.urls)),
]

# create views for the app
def login(request):
    return render(request, 'account/login.html', {})

# Create respective templates > appname > html file
Goto appname > create folder templates > create folder appname > create file html

# If we want to create base files, create them in ProjectLevel templates
ProductHunt( where settings.py lives ) > templates > base.html
{% block block_name %}
{% endblock %}

or

> templates > components > header.html, footer.html
{% include 'components/header.html' with islogin = True %}

# To get them working we need to include its path in DIRS in settings.py
'DIRS': ['ProductHunt/templates'],

# to use block_name use this tag : To copy the entire code between tag
{% extends 'base.html' %}
{% block content %}
    "shifting code to be here -- This code will be pasted in base template "
{% endblock %}

# to use code snippets to include in
{% include 'header.html' with variable=value person="Jane" islogin=True %} # This code will be pasted in current file
"Remaining code here"
# using the varaible we can customize the base template that we are including

# Static file structure for( All needs (likely Base ))
ProductHunt > static > images > files
ProductHunt > static > css > files
ProductHunt > static > js > files
# to use static files include it in settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'ProductHunt/static'
]
# In HTML we use these TEMPLATES
{% load static %}
{% static 'images/load.gif' %}


# ------------------------------------ Authentication Part ---------------------------------

# Apply and make migrations first
python manage.py makemigrations
python manage.py migrate

# Create super user
python manage.py createsuperuser

# enter username and password for admin

# user packages and login, logout, signup
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('account:signup')
        else:
            return render(request, 'account/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'account/login.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password-re']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'account/signup.html', {'error':'username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                auth.login(request,user)
                return redirect('account:login')
        else:
            return render(request, 'account/signup.html', {'error':'Passwords must match'})
    else:
        return render(request, 'account/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('account:login')


# -- templates for login / logout
# Use like this or use a seperate JS static file same as css
{% if user.is_authenticated %}
<a class="nav-item nav-link active" href="javascript:{document.getElementById('logout').submit()}" onclick="">Logout</a>
<form id="logout" method="POST" action="{% url 'account:logout' %}">
   {% csrf_token %}
   <input type="hidden" />
</form>
{% else %}
<a class="nav-item nav-link active" href="{% url 'account:login' %}">Login</a>
<a class="nav-item nav-link" href="{% url 'account:signup' %}">SignUp</a>
{% endif %}

# we can use
{% include 'base.html' islogin=True %}
#in our file

#in our base the code will be as this
<a class="nav-item nav-link {% if islogin %} active {% endif %}" href="{% url 'account:login' %}">Login</a>
<a class="nav-item nav-link {% if not islogin %} active {% endif %}" href="{% url 'account:signup' %}">SignUp</a>


# ------------------------------------ MODELS -----------------------------------------
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.title[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

# To use / connect the use to the model we use
from django.contrib.auth.models import User
user = models.ForeignKey(User, on_delete=models.CASCADE)

# If we need admin to enter, register model with admin
admin.site.register(Model)


# After creating models dont forget to migrate to database
python manage.py makemigrations
python manage.py migrate

# ---------------------------- Login Requiring -------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required(login_url="/account/signup") # resloves to localhost:8000/account/sidnup
# apply this decorator on the views for which we need to stop unauthenticated users

# if user type that url in bar .. he will be redirected to signup page with ?next=/product/create
http://localhost:8000/account/signup/?next=/product/create/

# saving a models user field
product = Product()
product.title = request.POST['title']
product.user = request.user
product.save()


# single object retreival
from django.shortcuts import render, redirect, get_object_or_404
product = get_object_or_404(Product, pk=product_id)


# Looping listener
{% for product in products %}
    <a href="javascript:{document.getElementById('upvote{{product.id}}').submit()}"><button  type="button" class="btn btn-sm btn-primary">Upvote {{product.votes_total}}</button></a>
    <form id="upvote{{product.id}}" method="POST" action="{% url 'product:upvote_wo' product.id %}">
        {% csrf_token %}
        <input type="hidden" />
    </form>
{% endfor %}
