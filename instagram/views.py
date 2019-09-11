from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static
from .models import SignUp,Posts,FriendList
def homepage(request):
        if request.method=="POST":
            a = request.POST.get('username')
            b = request.POST.get('Password')
            if SignUp.objects.filter(Username=a,Password=b).exists() is True:
                c = SignUp.objects.filter(Username=a).values_list('Number')[0][0]
                d = SignUp.objects.filter(Username=a).values_list('Email')[0][0]
                e = SignUp.objects.filter(Username=a).values_list('Image')[0][0]
                fs = FileSystemStorage()
                e = fs.url(e)
                request.session['username'] = a
                request.session['password'] = b
                request.session['number'] = c
                request.session['email'] = d
                request.session['profile'] = e
                return redirect('success')
            else:
                messages.error(request,"invalid username or password")
                return redirect('homepage')
    
        return render(request,'login.html',None)

def signup(request):
    if request.method == "POST":
        user = request.POST.get('username')
        pas = request.POST.get('Password')
        conpas = request.POST.get('confirmpassword')
        num = request.POST.get('Number')
        mail = request.POST.get('email')
        request.session['username'] = user
        request.session['profile'] = "default.jpg"
        request.session['number'] = num
        request.session['email'] = mail
        request.session['password'] = pas
        data1 = SignUp.objects.filter(Username=user)
        data2 = SignUp.objects.filter(Number=num)
        data3 = SignUp.objects.filter(Email=mail)
        if pas != conpas:
            messages.error(request,"password and confirm password doesn't match")
            return redirect('signup')
        elif SignUp.objects.filter(Username=user).exists() is True:
            messages.error(request,'user name already taken')
            return redirect('signup')
        elif SignUp.objects.filter(Number=num).exists() is True:
            messages.error(request,'number already taken')
            return redirect('signup')
        elif SignUp.objects.filter(Email=mail).exists() is True:
            messages.error(request,'mail id already exists')
            return redirect('signup')
        else:
            a = SignUp(Username = user,Password = pas,Number = num,Email = mail)
            a.save()
            return redirect('success')
    else:
        return render(request,'signup.html',None)
def logout(request):
    request.session.flush()
    return redirect('/')
def success(request):
    if len(request.session.keys()) != 0:
        a = request.session.get('profile')
        b = request.session.get('username')
        user = SignUp.objects.get(Username=b)
        Posts.objects.filter(User=user).update(Profile=a)
        friends = FriendList.objects.filter(Friend=user,Status="accepted")
        context = Posts.objects.filter(User=user)
        for post in friends:
            c = SignUp.objects.get(Username=post.Friend_name)
            context = context | Posts.objects.filter(User=c)
        context = context.order_by("-Date")
        li = SignUp.objects.values('Username')
        return render(request,'homepage.html',{'context':context,'li':li})
    else:
        return HttpResponse("session expired")
def friendrequest(request):
    if len(request.session.keys()) != 0:
        context = {}
        user = request.session.get('username')
        context = FriendList.objects.filter(Friend_name=user,Status=None)
        return render(request,'friendrequest.html',{'context':context})
    else:
        return HttpResponse("session expired")
def reject(request,username):
    a = SignUp.objects.get(Username=username)
    user = request.session.get('username')
    FriendList.objects.filter(Friend=a,Friend_name=user).update(Status='rejected')
    return redirect('friendrequest')
def add(request,username):
    a = SignUp.objects.get(Username=username)
    user = request.session.get('username')
    FriendList.objects.filter(Friend=a,Friend_name=user).update(Status='accepted')
    return redirect('friendrequest')
def profile(request):
    if len(request.session.keys()) != 0:
        context = {}
        username = request.session.get('username')
        number = request.session.get('number')
        email = request.session.get('email')
        ima = SignUp.objects.filter(Username=username).values_list('Image')[0][0]
        fs = FileSystemStorage()
        image = fs.url(ima)
        request.session['profile'] = image
        context = [{
            'Username':username,
            'Number':number,
            'Email':email,
            'Image': image
        }]
        li = SignUp.objects.values('Username')
        return render(request,'profile.html',{'context':context,'li':li})
    else:
        return HttpResponse("session expired")
def friends(request):
    if len(request.session.keys()) != 0:
        user = request.session.get('username')
        a = SignUp.objects.get(Username=user)
        context = FriendList.objects.filter(Friend=a,Status="accepted").order_by('Friend_name')
        return render(request,'view_friends.html',{'context':context})
    else:
        return HttpResponse("session expired")
def unfollow(request,friend_name):
    user = request.session.get('username')
    a = SignUp.objects.get(Username=user)
    FriendList.objects.filter(Friend=a,Friend_name=friend_name).delete()
    return redirect('view_friends')

def editprofile(request):
    if len(request.session.keys()) != 0:
        file = FileSystemStorage()
        username = request.session.get('username')
        password = request.session.get('password')
        number = request.session.get('number')
        email = request.session.get('email')
        a = SignUp.objects.get(Username=username)
        b = a.id
        image = SignUp.objects.filter(id=b).values_list('Image')[0][0]
        image = file.url(image)
        context = [{
            'Username':username,
            'Password':password,
            'Number':number,
            'Email':email,
            'Image':image
        }]
        if request.method == 'POST':
            user = request.POST.get('username')
            request.session['username'] = user
            password = request.POST.get('password')
            request.session['password'] = password
            number = request.POST.get('number')
            request.session['number'] = number
            mail = request.POST.get('mail')
            request.session['mail'] = mail
            SignUp.objects.filter(Username=username).update(Username=user,Password=password,Number=number,Email=mail)
            FriendList.objects.filter(Friend_name=username).update(Friend_name=user)
            try:
                a = request.FILES['user-profile']
                SignUp.objects.filter(Username=user).update(Image=a)
                name = file.save(a.name,a)
                request.session['profile'] = file.url(name)
            except MultiValueDictKeyError:
                request.session['profile'] = image
            return redirect('editprofile')
        return render(request,'editprofile.html',{'context':context})
    else:
        return HttpResponse("session expired")
def tweet(request):
    if len(request.session.keys()) != 0:
        context = {}
        if request.method == "POST":
            username = request.session.get('username')
            tweet = request.POST.get('tweet')
            image = SignUp.objects.filter(Username=username).values_list('Image')[0][0]
            file = FileSystemStorage()
            image = file.url(image)
            a = SignUp.objects.get(Username=username)
            b=Posts(User=a,Tweet=tweet,Profile=image)
            b.save()
            return redirect('home')
        return render(request,'tweet.html',context)
    else:
        return HttpResponse("session expired")
def video_posts(request):
    if len(request.session.keys()) != 0:
        if request.method == "POST":
            username = request.session.get('username')
            try:
                video_posts = request.FILES['posts_video']
                fs = FileSystemStorage()
                name = fs.save(video_posts.name,video_posts)
                url = fs.url(name)
                profile = request.session.get('profile')
            except MultiValueDictKeyError:
                messages.error(request,"select video to upload")
                return redirect('video_posts')
            a = SignUp.objects.get(Username=username)
            b = Posts(User=a,Profile=profile,Posts_video=url)
            b.save()
            return redirect('success')
            
        return render(request,'posts_video.html',{})
    else:
        return HttpResponse("session expired")
def posts_image(request):
    if len(request.session.keys()) != 0:
        context = {}
        if request.method == "POST":
            username = request.session.get('username')
            try:
                img_post = request.FILES['posts_image']
                fs = FileSystemStorage()
                name = fs.save(img_post.name,img_post)
                url = fs.url(name)
                profile = request.session.get('profile')
            except MultiValueDictKeyError:
                messages.error(request,"select an image to upload")
                return redirect('posts_image')
            a = SignUp.objects.get(Username=username)
            b = Posts(User=a,Profile=profile,Posts_image=url)
            b.save()
            return redirect('success')
        return render(request,'posts_image.html',context)
    else:
        return HttpResponse("session expired")

def profile_view(request,username):
    if len(request.session.keys()) != 0:
        view = {}
        request.session['friend'] = username
        user = request.session.get('username')
        friend = request.session.get('friend')
        if user != friend:
            view['flag'] = 1
        context = SignUp.objects.filter(Username=username)
        return render(request,'profile_view.html',{'context':context,'view':view})
    else:
        return HttpResponse("session expired")
def sentrequest(request):
    friend = request.session.get('friend')
    user = request.session.get('username')
    a = SignUp.objects.get(Username=user)
    check = FriendList.objects.filter(Friend=a).values_list('Friend_name',flat="True")
    status = FriendList.objects.filter(Friend=a).values_list('Status',flat="True")
    for i in range(len(check)):
        if check[i] == friend:
            if status[i] == 'rejected':
                FriendList.objects.filter(Friend=a,Friend_name=friend).update(Status=None)
                messages.success(request,"friend request send")
                return redirect('user_view',friend)
            messages.error(request,'friend request already send')
            return redirect('user_view',friend)
    else:
        b = FriendList(Friend=a,Friend_name=friend)
        b.save()
        messages.success(request,"friend request send")
        return redirect('user_view',friend)
    
