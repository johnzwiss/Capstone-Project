from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import LoginForm

# Create your views here.

# login view
def login_view(request):
    # we can use the same view for multiple HTTP requests
    # this can be done with a simple if statement
    if request.method == 'POST':
        # handle post request
        # we want to authenticate the user with the username and pw
        form = LoginForm(request.POST)
        # validate the form data
        if form.is_valid():
            # get the username and pw and save them to variables
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            # here we use django's built in authenticate method
            user = authenticate(username = u, password = p)
            # if you found a user with matching credentials
            if user is not None:
                # if that user has not been disabled by admin
                if user.is_active:
                    # use django's built in login function
                    login(request, user)
                    return HttpResponseRedirect('/user/' + str(user.username))
                else:
                    print('the account has been disabled')
            else:
                print('the username or password is incorrect')
    else:
        # the request is a get, we render the login page
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# logout view
def logout_view(request):
    # print('####### THIS IS THE REQUEST #######')
    # print(request.user)
    logout(request)
    return HttpResponseRedirect('/')

# signup view
def signup_view(request):
    # if the req is a post, then sign them up
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/' + str(user.username))
    # if the req is a get, then show the form
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})