from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('signup',views.signup,name='signup'),
    path('success/',views.success,name='success'),
    path('success/home',views.success,name='home'),
    path('success/logout',views.logout,name='logout'),
    path('success/friendrequest',views.friendrequest,name="friendrequest"),
    path('success/posts_image',views.posts_image,name='posts_image'),
    path('success/video_posts',views.video_posts,name='video_posts'),
    path('success/tweet',views.tweet,name='tweet'),
    path('success/profile',views.profile,name='profile'),
    path('success/view_friends',views.friends,name='view_friends'),
    path('success/unfollow?<friend_name>',views.unfollow,name='unfollow'),
    path('success/editprofile',views.editprofile,name='editprofile'),
    path('success/user_view?<username>',views.profile_view,name='user_view'),
    path('success/reject<username>',views.reject,name='reject'),
    path('success/add<username>',views.add,name='add'),
    path('success/sentrequest',views.sentrequest,name='sentrequest'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
