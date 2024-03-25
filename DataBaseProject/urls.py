"""
URL configuration for DataBaseProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.initial),
    #user
    path('user/login/', views.user_login),
    path('user/signup/', views.user_signup),
    path('user/home/',views.user_home,name='user/home'),
    path('user/movie/', views.user_movie, name='user_movie'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('myspace/',views.myspace, name='myspace'),
    #director
    path('manager/director/', views.manager_director),
    path('manager/director_add/', views.manager_director_add),
    path('manager/director_delete/', views.manager_director_delete),
    path('manager/director_update/', views.manager_director_update),
    #movie
    path('manager/movie/', views.manager_movie),
    path('manager/movie_add/', views.manager_movie_add),
    path('manager/movie_delete/',views.manager_movie_delete),
    path('manager/movie_update/', views.manager_movie_update),
    # user
    path('manager/user/', views.manager_user),
    path('manager/user_add/', views.manager_user_add),
    path('manager/user_delete/', views.manager_user_delete),
    path('manager/user_update/', views.manager_user_update),
    # review
    path('manager/review/', views.manager_review),
    path('manager/review_add/', views.manager_review_add),
    path('manager/review_delete/', views.manager_review_delete),
    path('manager/review_update/', views.manager_review_update),
    # like
    path('manager/like/', views.manager_like),
    path('manager/like_add/', views.manager_like_add),
    path('manager/like_delete/', views.manager_like_delete),
    # actor
    path('manager/actor/', views.manager_actor),
    path('manager/actor_add/', views.manager_actor_add),
    path('manager/actor_delete/', views.manager_actor_delete),
    path('manager/actor_update/', views.manager_actor_update),
    # cast
    path('manager/cast/', views.manager_cast),
    path('manager/cast_add/', views.manager_cast_add),
    path('manager/cast_delete/', views.manager_cast_delete),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


