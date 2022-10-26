import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, SignUpForm, PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from .models import Post
from django.contrib.auth.models import Group
#  Create your views here.

 
#home
def home(request):
    posts=Post.objects.all()
    # user_name_mention=request.user
    gps=request.user.groups.all()
    # print(posts)
    return render(request,'blog/home.html',{'posts': posts,'groups':gps})  #here there is no use of gps in html so no worries!!
#about
def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    return render(request,'blog/contact.html')

#dashboard
@login_required(login_url='/login')
def Dashboard(request,id):
    # if request.user.is_authenticated(): # we can use this var either but at above we have already used decorators
    # uname=request.user.username
    if id==1:
        posts=Post.objects.all()
        user=request.user
        fullname=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts': posts, 'fullname':fullname, 'groups': gps})

    posts=Post.objects.filter(user=id)
    user=request.user
    fullname=user.get_full_name()
    gps=user.groups.all()
    return render(request,'blog/dashboard.html',{'posts': posts, 'fullname':fullname, 'groups': gps})

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        # print(form)
        # print()
        # print(request.POST)
        if form.is_valid():
            messages.success(request,'Account successfully created. You have become an author')
            user=form.save()
            group= Group.objects.get(name='Author')
            user.groups.add(group)            
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

#login
# uid=None
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)  # Agar uname and upass kraane se authenticate ho jaata hai to hame user object mil jaayega.
                if user is not None:
                    login(request, user)
                    global uid
                    uid=user.get_username 
                    messages.success(request,'Logged in successfully!!')
                    return HttpResponseRedirect('/dashboard/{id}/'.format(id=user.id))
        else:
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


# Update new Post 
def update_post(request,id):
     if request.user.is_authenticated:
         if request.method == 'POST':
             data=Post.objects.get(id=id)
             newform=PostForm(request.POST,instance=data)
             form=newform
             if form.is_valid():
                 form.save()
                 messages.success(request,'Post id --{id}-- Updated Succesfully!!!'.format(id=id))
                 return HttpResponseRedirect('/dashboard/{id}'.format(id=request.user.id))
         else:
             data=Post.objects.get(id=id)
             oldform=PostForm(instance=data)  
             form=oldform
         return render (request,'blog/updatepost.html',{'form':form})
     
     else: HttpResponseRedirect('/login/')
 
#Add Post
def add_post(request):
     if request.user.is_authenticated:
         if request.method == 'POST':
             postform=PostForm(request.POST)
             if postform.is_valid():
                #  postform.save()   #here we are directly saving data that has been coming through form into my table named as Post(also we can say a model)
                #  title=postform.cleaned_data['title'] # But lets save our data using cleaned_data method so that i can understand two ways to understand data
                #  desc=postform.cleaned_data['desc']
                #  user=request.user.id
                #  pst= Post(title=title, desc=desc)
                 pst=postform.save(commit=False)
                 pst.user=request.user
                 print(pst.user)
                #  pst= Post(title=title, desc=desc)
                 pst.save()
                 messages.success(request,'New Post Added')
                 postform=PostForm() #making our form blank so that our second add data can be stored
         else: 
             postform=PostForm()
         return render (request,'blog/addpost.html',{'form':postform})
     
     else: HttpResponseRedirect('/login/')

def delete_post(request,id):
     if request.user.is_authenticated:
         if request.method == 'POST':
             data=Post.objects.get(id=id)
             data.delete()
         return HttpResponseRedirect('/dashboard/{id}'.format(id=request.user.id))
     
     else: return HttpResponseRedirect('/login/')