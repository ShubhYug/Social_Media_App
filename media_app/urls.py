from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
# from django.conf import settings
# from django.conf.urls.static import static



urlpatterns =[
    
    path('',views.index,name='index'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),


    path('profile/',views.profile,name='profile'),
    path('create_profile/',views.create_profile,name='create_profile'),
    # path('update_profile/<int:id>/',views.update_profile,name='update_profile'),
    path('registration/',views.registration,name='registration'),
    path('delete_data/<int:id>/',views.delete_data,name='delete_data'),
    path('show_profile/',views.show_profile,name='show_profile'),
    path('show_data/',views.show_data,name='show_data'),
    path('edit_profile/<int:id>/',views.edit_profile,name='edit_profile'),
    path('edit_bio/<int:id>/',views.edit_bio,name='edit_bio'),
    path('friend_profile/<int:id>/',views.friend_profile,name='friend_profile'),
    path('my_friend/',views.my_friend,name='my_friend'),
    path('remove_friend/<int:id>/',views.remove_friend,name='remove_friend'),

    path('my_post/',views.my_post,name='my_post'),
    path('create_post/',views.create_post,name='create_post'),
    path('delete_post/<int:id>/',views.delete_post,name='delete_post'),
    path('edit_post/<int:id>/',views.edit_post,name='edit_post'),
    path('show_post/',views.show_post,name='show_post'),
    path('my_friend_post/',views.my_friend_post,name='my_friend_post'),
    path('delete_post/<int:id>/',views.delete_post,name='delete_post'),


    # path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    # path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),

    path('update_comment/<int:id>/', views.update_comment, name='update_comment'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('comment_post/<int:id>/', views.comment_post, name='comment_post'),
    path('show_comment/<int:id>/', views.show_comment, name='show_comment'),

    # path('edit_comment/<int:id>/', views.edit_comment, name='edit_comment'),
    # path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),

    path('like_post/<int:id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:id>/', views.dislike_post, name='dislike_post'),
    path('like_count/<int:id>/', views.like_count, name='like_count'),

    path('all_dislike_post/<int:id>/', views.all_dislike_post, name='all_dislike_post'),
    path('all_like_post/<int:id>/', views.all_like_post, name='all_like_post'),
    # path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),

    path('friends/',views.friends, name= 'friends'),
    # path('all_pepoles/',views.all_pepoles, name= 'all_pepoles'),
    path('send_request/<int:to_user_id>/', views.send_request, name='send_request'),
    path('all_request/', views.all_request, name='all_request'),
    path('my_friend/', views.my_friend, name='my_friend'),
    path('my_friend_search/', views.my_friend_search, name='my_friend_search'),
    path('friend_search/', views.friend_search, name='friend_search'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)