from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm,SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models import Q

from .forms import UserForm, PostForm,CommentForm,UserRegisterForm,ProfileForm
from .models import Post, Profile,Comment,Like,FriendRequest,Message


#home page
def index(request):
    # return render(request,'social/index01.html')
    return render(request,'social/profile.html')


#-----------------------User profile CRUD----------------------------------------------------------------


#Create/ registration
def registration(request):
    if request.method == 'POST':
        # breakpoint()
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/show_data')
    else:  
        form = UserForm()  
    return render(request,'social/registration.html',{'form':form})  

@login_required(login_url='/login/')
def create_profile(request):
    # user = User.objects.get(id = id)
    if request.method == 'POST':
        # breakpoint()
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/show_data')
    else:  
        form = ProfileForm()  
    return render(request,'social/edit_profile.html',{'form':form})  



#user profile
@login_required(login_url='/login/')
def profile(request):
    user =  request.user
    form = User.objects.filter(username = user)
    # j = form.id
    profile_form = PostForm()
    profile =  Profile.objects.filter(id = user.id)
    send_req = FriendRequest.objects.filter(from_user = request.user, accepted = False)
    rececive_req = FriendRequest.objects.filter(to_user = request.user, accepted = False)

    # show_borrow = Borrow.query.filter(Borrow.user_id == current_user.id).all()
    print(user,'--------------',form,'------------',profile,'------------')
    context = {
                'form':form,
                'profile':profile, 
               'profile_form':profile_form,
               'send_req':send_req,
               'rececive_req':rececive_req
               } 
    return render(request,"social/profile.html",context)


#Read user
@login_required(login_url='/login/')
def show_data(request):  
    form = User.objects.all() 
    profile = Profile.objects.all()
    context = {'form':form,'profile':profile }
    return render(request,"social/show_data.html",context)  


 
@login_required(login_url='/login/')
def show_profile(request):  
    user =  request.user
    form1 = User.objects.filter(username = request.user)
    form =  Profile.objects.filter(user = user)
    context = {'form':form,'form1':form1} 
    return render(request,"social/user_profile.html",context) 





#Update profile
@login_required(login_url='/login/')
def edit_profile(request, id):
    user = Profile.objects.get(user = id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('show_profile')
    else:
        form = ProfileForm(instance = user)
        context = {'form':form} 
        return render(request,"social/edit_profile.html",context) 


# #Update
@login_required(login_url='/login/')
def edit_bio(request, id):
    user = User.objects.get(id = id)
    form = UserForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect('/show_data')
    
    context = {'student':user} 
    return render(request,"social/edit_post.html",context) 

#Delete
@login_required(login_url='/login/')
def delete_data(request, id):
    form = User.objects.get(id = id)
    form.delete()
    return redirect('/show_data') 



#-----------------------Frined Request send & accept----------------------------------------------------------------


@login_required(login_url='/login/')
def friends(request):
    User = get_user_model()
    current_user = request.user
    friends = FriendRequest.objects.filter(from_user=current_user, accepted=True) | FriendRequest.objects.filter(to_user=current_user, accepted=True)
    friends_users = [friend.from_user if friend.to_user == current_user else friend.to_user for friend in friends]
    
    # Exclude users who are already in your friend list
    new_friends = User.objects.exclude(id__in=[user.id for user in friends_users]).exclude(id=current_user.id)
    return render(request,'social/friends.html',{'friend':new_friends })

#show select friend profile
@login_required(login_url='/login/')
def friend_profile(requset,id):
    user = User.objects.filter(id = id)
    profile = Profile.objects.filter(user_id = id).order_by('-id')
    context = {'form':profile,'form1':user} 
    return render(requset,"social/friend_profile.html",context)


#only show my friends
@login_required(login_url='/login/')
def my_friend(request):
    user  = request.user
    form = FriendRequest.objects.filter(Q(from_user = request.user.id) | Q(to_user = request.user.id) ,accepted = True).all()
    context = {'form':form}

    friends = []
    for frm in form:
        if frm.from_user.username == user.username:
            friends.append(frm.to_user)
        else:
            friends.append(frm.from_user)
    context = {'friend':friends}
    return render(request,"social/my_friends.html",context)



@login_required(login_url='/login/')
def send_request(request, to_user_id):
    to_user = get_object_or_404(User,id = to_user_id)
    FriendRequest.objects.get_or_create(from_user = request.user, to_user = to_user)
    return redirect('friends')

@login_required(login_url='/login/')
def accept_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id = request_id, to_user = request.user )
    friend_request.accepted = True
    friend_request.save()
    return redirect('all_request')

@login_required(login_url='/login/')
def reject_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id = request_id, to_user = request.user )
    friend_request.delete()
    return redirect('all_request')


#request accept and sent notification on html page
@login_required(login_url='/login/')
def all_request(request):
    rececive_req = FriendRequest.objects.filter(to_user = request.user, accepted = False)
    send_req = FriendRequest.objects.filter(from_user = request.user, accepted = False)
    return render(request,'social/request.html',{'form':rececive_req, 'form1':send_req})


@login_required(login_url='/login/')
def remove_friend(request,id):
    current_user = request.user
    friend = FriendRequest.objects.filter(from_user_id = id,to_user_id = current_user,accepted = True) | FriendRequest.objects.filter(to_user_id = id, from_user_id = current_user, accepted = True)
    friend.accepted = False
    friend.delete()
    return redirect('my_friend')



#All Friend search
@login_required(login_url='/login/')
def friend_search(request):
    if request.method == 'POST':
        friend_search = request.POST.get('friend_search')
        friends = User.objects.filter(first_name__icontains=friend_search).all()
        print(friends,'================================')
        context = {'friend':friends}
        return render(request,"social/friends.html",context)
    return redirect('friends')

#My friends search
@login_required(login_url='/login/')
def my_friend_search(request):
    if request.method == 'POST':
        friend_search = request.POST.get('my_friend_search')
        friends = User.objects.filter(first_name__icontains=friend_search).all()
        print(friends,'================================')
        context = {'friend':friends}
        return render(request,"social/my_friends.html",context)
    return redirect('my_friend')

#-----------------------Post like comment----------------------------------------------------------------


#create post
@login_required(login_url='/login/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate the post with the current user
            post.save()
            return redirect('my_friend_post')
    else:
        form = PostForm()
    return render(request,'social/create_post.html',{'form':form})


# @login_required
# def show_post(request):
#     posts = Post.objects.annotate(like_count=Count('likes')).all()
#     # posts = Post.objects.annotate(like_count=Count('likes')).all()
#     count = Like.objects.annotate(like_post=Count('likes')).all()

#     print(count,'=====================================================')
#     print(str(posts.query))

#     return render(request, "social/post_list_all.html", {'form': posts})


    # posts = Post.objects.annotate(like_count=Count('likes')).all()
    # print(user,'=user=======================')
    # print(count.User,'=likeaction=======================')
    # # print(form,'=form=======================')

#show all post
@login_required(login_url='/login/')
def show_post(request):  
    user = request.user.id
    form = Post.objects.all().order_by('-id')
    like_action = Like.objects.filter(user_id = user, liked_post__in = form).values_list('liked_post_id',flat=True)
    count = Like.objects.filter(user_id = user).count()
    # count = Like.objects.filter(liked_post_id = form).count()
    print(count,'=likeaction============user=',user,'===============like=',like_action)
    context = {
        'form':form,
        'like_action':like_action,
        'count':count
               } 
    return render(request,"social/post_list_all.html",context) 



#show Friends post only
@login_required(login_url='/login/')
def my_friend_post(request):  
    user = request.user.id
    friends = FriendRequest.objects.filter(from_user_id = user,accepted = True) | FriendRequest.objects.filter(to_user_id = user, accepted = True)
    friend_users = [friend.from_user_id if friend.to_user_id == request.user else friend.to_user_id for friend in friends]
    form = Post.objects.filter(user_id__in = friend_users).order_by('-id')

    #like post and auto disable unlike button
    like_action = Like.objects.filter(user_id = user, liked_post__in = form).values_list('liked_post_id',flat=True)
    count = Like.objects.filter(user_id = user).count()
    print(like_action,'======================================================================')
    context = {
        'form':form,
        'like_action':like_action,
        'count':count
        } 
    return render(request,"social/post_list.html",context) 

#my post 
@login_required(login_url='/login/')
def my_post(request):
    user = Post.objects.filter(user_id = request.user).all()
    context = {'form':user} 
    return render(request,"social/my_post.html",context) 



#edit post 
@login_required(login_url='/login/')
def edit_post(request, id):
    user = Post.objects.get(id = id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('my_post')
    else :
        form = PostForm(instance = user)
        context = {'form':form} 
        return render(request,"social/edit_post.html",context) 



#Delete post
@login_required(login_url='/login/')
def delete_post(request, id):
    form = Post.objects.get(id = id)
    form.delete()
    return redirect('/show_post') 


#friends like
@login_required(login_url='/login/')
def like_post(request, id):
    post = get_object_or_404(Post,id = id)
    like = Like.objects.filter(user = request.user.id, liked_post = post).exists()
    if not like:
        like1 = Like(user = request.user, liked_post = post)
        like1.save()
    return redirect('my_friend_post')


#freinds dislike
@login_required(login_url='/login/')
def dislike_post(request, id):
    post = get_object_or_404(Post,id = id)
    like = Like.objects.filter(user = request.user, liked_post = post).first()
    if like:
        like.delete()
    return redirect('my_friend_post')



#all post like and dislike option
@login_required(login_url='/login/')
def all_like_post(request, id):
    post = get_object_or_404(Post,id = id)
    like = Like.objects.filter(user = request.user.id, liked_post = post).exists()
    if not like:
        like1 = Like(user = request.user, liked_post = post)
        like1.save()
    return redirect('show_post')

#public Dislike
@login_required(login_url='/login/')
def all_dislike_post(request, id):
    post = get_object_or_404(Post,id = id)
    like = Like.objects.filter(user = request.user, liked_post = post).first()
    if like:
        like.delete()
    return redirect('show_post')




@login_required(login_url='/login/')
def like_count(request,id):
    post = get_object_or_404(Post,id = id)
    like = Like.objects.filter(liked_post = post).count()
    print(like,'======================================')
    return render(request,'social/post_list.html',{'like':like})



#-----------------------Commnet CRUD---------------------------------------------------------------------


@login_required(login_url='/login/')
def comment_post(request, id):
    post = get_object_or_404(Post, id = id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('show_post')
        
            # return redirect('show_comment', post_id = id)
    else:
        form = CommentForm()
    return render(request, 'social/post_detail.html', {'form': form})


@login_required(login_url='/login/')
def show_comment(request,id):
    post = Post.objects.filter(id=id).all()
    # return render(request,"social/post_list.html",context) 

    show = Comment.objects.filter(post_id=id).all()
    context = {'post':post,'form':show} 
    return render(request,'social/comment.html',context)


@login_required(login_url='/login/')
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id = id)
    comment.delete()
    return redirect('show_post')


@login_required(login_url='/login/')
def update_comment(request, id):
    post = get_object_or_404(Comment, id = id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('show_post')
            # return redirect('show_comment', post_id = id)
    else:
        form = CommentForm(instance=post)
    return render(request, 'social/comment.html', {'form2': form})


#-----------------------Message sent & receive-------------------------------------------------------------------


@login_required
def send_message(request, receiver_id):
    # id
    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        receiver = User.objects.get(id=receiver_id)
        
        message = Message.objects.create(sender=sender, receiver=receiver, content=content)
        return redirect('inbox')  # Redirect to the inbox or any other appropriate page

@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'social/inbox.html', {'received_messages': received_messages})



#-----------------------login & Logout-------------------------------------------------------------------

#login
def login_user(request):
    # if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request = request,data = request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'] 
                userpass = form.cleaned_data['password']

                user=authenticate(username = username, password =userpass)     
                print('======11',user,'======')
                if user is not None:
                    print('======22',user,'======')
                    login(request, user)
                    # login(request,user) Link
                    print('======33',user,'======')
                    messages.success(request, 'logged is successfully ??')
                    
                    return redirect('profile') 
        else:
            form = AuthenticationForm() 
        return render(request, 'social/login.html', {'form':form}) 
    # else:
    #     return redirect('/index/') 


#logout
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('login')