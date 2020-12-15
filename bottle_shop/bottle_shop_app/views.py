from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Bottle, Message, Comment
from django.core.files.storage import FileSystemStorage
from .forms import BottleForm

## RENDER
def log_reg(request):
    return render(request, "log_reg.html")
def my_profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'my_profile.html', context)
def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, "profile.html", context)
def bottle_shop_dash(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'all_messages': Message.objects.all(),
    }
    return render(request, 'bottle_shop_dash.html', context)  

## LOG AND REG
def login(request):
    if request.method=="POST":
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['full_name']=f"{logged_user.first_name} {logged_user.last_name}"
                request.session['location']=logged_user.location
                return redirect('/bottle_shop_dash')
    return redirect('/')
def register(request):
    if request.method=='POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], date_of_birth=request.POST['date_of_birth'], location=request.POST['location'], about=request.POST['about'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['full_name']=f"{new_user.first_name} {new_user.last_name}"
        request.session['location']=new_user.location
        request.session['about']=new_user.about
        return redirect('/bottle_shop_dash')
    return redirect('/')

## EDIT PROFILE
def edit_profile(request, user_id):
    edit_profile = User.objects.get(id=user_id)
    context = {
        'profile': edit_profile
    }
    return render(request, 'edit_profile.html', context)
def update_profile(request, user_id):
    if request.method=="POST":
        errors = User.objects.profile_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f'/my_profile/{user_id}')
        # email_error = User.objects.email_edit_validator(request.POST)
        # if email_error:
        #     for error in email_error:
        #         messages.error(request, email_error[error])
        #     return redirect(f'/edit_profile/{profile_id}')
        to_update=User.objects.get(id=user_id)
        to_update.first_name=request.POST['first_name']
        to_update.last_name=request.POST['last_name']
        to_update.email=request.POST['email']
        to_update.date_of_birth=request.POST['date_of_birth']
        to_update.password=request.POST['password']
        to_update.about=request.POST['about']
        to_update.save()
        return redirect('/bottle_shop_dash')
    return redirect('/bottle_shop_dash')

## RENDER ADD BOTTLE PAGE/UPLOAD BOTTLE
def add_bottle(request):
    if request.method == "POST":
        form = BottleForm(request.POST, request.FILES,)
        if form.is_valid():
            add_to_user = request.session['user_id']
            form.owner=add_to_user
            form.save()
            return redirect('/bottle_shop_dash') 
        # HOW TO RETURN TO PROFILE PAGE??
    else:
        form = BottleForm()
    return render(request, 'add_bottle.html', {
        'form': form
    })
# def upload_bottle(request):
#     form = BottleForm(request.POST, request.FILE)
#     return render(request, 'my_profile.html', {
#         'form': form
#     })


# def upload_prof_photo(request):
#     if request.method == "POST":
#         uploaded_file = request.FILES['prof_photo']
#         print(uploaded_file.name)
#         print(uploaded_file.size)
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file)
#     return redirect('/bottle_shop_dash')

## CREATE MESSAGE
def post_message(request):
    if request.method=="POST":
        errors = Message.objects.message_validator(request.POST)
        for error in errors:
            messages.error(request, errors[error])
            return redirect('/bottle_shop_dash')
        Message.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/bottle_shop_dash')
    return redirect('/bottle_shop_dash')

## LIKE/COMMENT
def like_message(request, message_id):
    liked_message = Message.objects.get(id=message_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/bottle_shop_dash')

def create_comment(request):
    if request.method=="POST":
        Comment.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']), message=Message.objects.get(id=request.POST['message']))
        return redirect('/bottle_shop_dash')
    return redirect('/bottle_shop_dash')

## DELETE
def comm_delete(request, comm_id):
    Comment.objects.get(id=comm_id).delete()
    return redirect('/bottle_shop_dash')
def mess_delete(request, mess_id):
    Message.objects.get(id=mess_id).delete()
    return redirect('/bottle_shop_dash')

## LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')

