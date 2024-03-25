from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings
import hashlib
import os

import app1
from .models import Review, Movie, User, Like, Director,Actor,Cast


def initial(request):
    return redirect("/user/login")

#用户界面-----------------------------------------------------------------------------
def user_login(request):
    method = request.method
    if method == "GET":
        return render(request, "user/login.html")
    elif method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            user_id = user.id
            res = password + settings.SECRET_KEY
            password = hashlib.md5(res.encode("utf-8")).hexdigest()
            if password == user.password:
                if user.username == "manager":
                    return redirect("/manager/director/")
                else:
                    return redirect(f"/user/home/?user_id={user_id}")
            else:
                return render(request, "user/login.html", {"tip": "密码错误！"})
        except app1.models.User.DoesNotExist:
            return render(request, "user/login.html", {"tip": "用户名不存在！"})


def user_signup(request):
    if request.method == "GET":
        return render(request, "user/signup.html")
    elif request.method == "POST":
        get_post = request.POST
        username = get_post.get("username")
        password = get_post.get("password")
        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()
        gender = get_post.get("gender")
        if User.objects.filter(username=username).exists():
            return render(request, "user/signup.html", {"msg": "注册失败，用户名已存在!"})
        else:
            User.objects.create(username=username, password=password, gender=gender)
            return redirect("/user/login/", {"tip2": "注册成功！"})


def user_home(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        return render(request, 'user/home.html', {'movies': movies, "user": user})
    if request.method == "POST":
        search_query = request.POST.get('search')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        movies = Movie.objects.filter(
            Q(moviename__icontains=search_query) |  # 电影名称模糊搜索
            Q(director__directorname__icontains=search_query) |  # 导演名称模糊搜索
            Q(type__icontains=search_query) |  # 类型模糊搜索
            Q(time__icontains=search_query) |  # 时间模糊搜索
            Q(area__icontains=search_query))  # 地区模糊搜索
        return render(request, 'user/home.html', {'movies': movies, "user": user, "search_query": search_query})


def user_movie(request):
    if request.method == "GET":
        movie_id = request.GET.get('movie_id')
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        movie = Movie.objects.get(id=movie_id)
        director = movie.director
        reviews = Review.objects.filter(movie=movie)
        cast_list = Cast.objects.filter(movie=movie)
        actors = [cast.actor for cast in cast_list]

        context = {
            'movie': movie,
            'director': director,
            'user': user,
            'reviews': reviews,
            'actors': actors
        }
        return render(request, 'user/movie.html', context)


def add_to_favorites(request):
    if request.method == 'POST' and request.is_ajax():
        movie = request.POST.get('movie')
        user = request.POST.get('user')
        movie = Movie.objects.get(id=movie)
        user = User.objects.get(id=user)
        Like.objects.create(user=user, movie=movie)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def add_comment(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating')
        movie = Movie.objects.get(id=movie_id)
        user = User.objects.get(id=user_id)
        Review.objects.create(user=user, movie=movie, comment=comment_text, rating=rating)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': '无效的请求'}, status=400)


def myspace(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    # 获取用户喜欢的电影
    likes = Like.objects.filter(user=user)
    liked_movies = [like.movie for like in likes]
    # 获取用户的评论
    reviews = Review.objects.filter(user=user)
    context = {
        'user': user,
        'movies': liked_movies,
        'reviews': reviews,
    }
    return render(request, 'user/myspace.html', context)


# 导演——————————————————————————————————————————————————————————————————
def manager_director(request):
    if request.method == "GET":
        director_list = Director.objects.all()
        return render(request, "manager/director.html", {"director_list": director_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        director_list = Director.objects.filter(
            Q(directorname__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(birthday__icontains=search_query) |
            Q(nationality__icontains=search_query))
        return render(request, 'manager/director.html', {'director_list': director_list,  "search_query": search_query})


def manager_director_add(request):
    method = request.method
    if method == "GET":
        return render(request, "manager/director_add.html")
    elif method == "POST":
        directorname = request.POST.get("directorname")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        nationality = request.POST.get("nationality")
        bio = request.POST.get("bio")
        photo = request.FILES.get("photo")
        Director.objects.create(directorname=directorname, gender=gender, birthday=birthday, nationality=nationality,
                                bio=bio, photo=photo)
        return redirect("/manager/director/")


def manager_director_delete(request):
    del_id = request.GET.get("del_id")
    director = Director.objects.filter(id=del_id).first()  # 获取要删除的 Director 实例
    if director.photo:
        photo_path = director.photo.path  # 获取文件的服务器路径
        if os.path.isfile(photo_path):  # 确保文件存在
            os.remove(photo_path)  # 删除文件
    director.delete()  # 删除 Director 实例
    return redirect("/manager/director/")


def manager_director_update(request):
    if request.method == "GET":
        update_id = request.GET.get("update_id")
        print("**", update_id)
        director = Director.objects.filter(id=update_id).first()
        return render(request, "manager/director_update.html", {"director": director})
    elif request.method == "POST":
        director_id = request.POST.get("director_id")
        directorname = request.POST.get("directorname")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        nationality = request.POST.get("nationality")
        bio = request.POST.get("bio")
        Director.objects.filter(id=director_id).update(directorname=directorname)
        Director.objects.filter(id=director_id).update(gender=gender)
        Director.objects.filter(id=director_id).update(birthday=birthday)
        Director.objects.filter(id=director_id).update(nationality=nationality)
        Director.objects.filter(id=director_id).update(bio=bio)
        return redirect("/manager/director/")


# 电影——————————————————————————————————————————————————————————————————
def manager_movie(request):
    if request.method == "GET":
        movie_list = Movie.objects.all()
        return render(request, "manager/movie.html", {"movie_list": movie_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        movie_list = Movie.objects.filter(
            Q(moviename__icontains=search_query) |  # 电影名称模糊搜索
            Q(director__directorname__icontains=search_query) |  # 导演名称模糊搜索
            Q(type__icontains=search_query) |  # 类型模糊搜索
            Q(time__icontains=search_query) |  # 时间模糊搜索
            Q(area__icontains=search_query))  # 地区模糊搜索
        return render(request, 'manager/movie.html', {'movie_list': movie_list,  "search_query": search_query})


def manager_movie_add(request):
    if request.method == "GET":
        directors = Director.objects.all()
        return render(request, "manager/movie_add.html", {"directors": directors})
    elif request.method == "POST":
        moviename = request.POST.get("moviename")
        director_id = request.POST.get("director")  # 注意，这里我们假设传入的是导演的ID
        movie_type = request.POST.get("type")
        time = request.POST.get("time")
        area = request.POST.get("area")
        length = request.POST.get("length")
        web = request.POST.get("web")
        bio = request.POST.get("bio")
        photo = request.FILES.get("photo")
        director = Director.objects.get(id=director_id)
        Movie.objects.create(moviename=moviename, director=director, type=movie_type,
                             time=time, area=area, length=length, web=web, bio=bio, photo=photo
                             )
        return redirect("/manager/movie/")


def manager_movie_delete(request):
    del_id = request.GET.get("del_id")
    movie = Movie.objects.filter(id=del_id).first()  # 获取要删除的 Movie 实例
    if movie.photo:
        photo_path = movie.photo.path  # 获取文件的服务器路径
        if os.path.isfile(photo_path):  # 确保文件存在
            os.remove(photo_path)  # 删除文件
    movie.delete()  # 删除 Movie 实例
    return redirect("/manager/movie/")  # 重定向到电影管理页面


def manager_movie_update(request):
    if request.method == "GET":
        update_id = request.GET.get("update_id")
        movie = Movie.objects.filter(id=update_id).first()
        directors = Director.objects.all()
        return render(request, "manager/movie_update.html", {"movie": movie, "directors": directors})
    elif request.method == "POST":
        movie_id = request.POST.get("movie_id")
        moviename = request.POST.get("moviename")
        director_id = request.POST.get("director")  # 注意这里假设传过来的是导演的ID
        type = request.POST.get("type")
        time = request.POST.get("time")
        area = request.POST.get("area")
        length = request.POST.get("length")
        web = request.POST.get("web")
        bio = request.POST.get("bio")
        # 更新电影实例
        Movie.objects.filter(id=movie_id).update(moviename=moviename, director_id=director_id,  # 注意这里是 director_id
                                                 type=type, time=time, area=area, length=length, web=web, bio=bio
                                                 )
        # 处理图片上传
        photo = request.FILES.get("photo")
        if photo:
            movie = Movie.objects.get(id=movie_id)
            movie.photo.save(photo.name, photo)

        return redirect("/manager/movie/")


# 用户管理-------------------------------------------------------------------------

def manager_user(request):
    if request.method == "GET":
        user_list = User.objects.all()
        return render(request, "manager/user.html", {"user_list": user_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        user_list = User.objects.filter(
            Q(username__icontains=search_query)|
            Q(gender__icontains=search_query))
        return render(request, 'manager/user.html', {'user_list': user_list, "search_query": search_query})


# 添加用户
def manager_user_add(request):
    if request.method == "GET":
        return render(request, "manager/user_add.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        gender = request.POST.get("gender")

        # 对密码进行加密
        res = password + settings.SECRET_KEY
        password = hashlib.md5(res.encode("utf-8")).hexdigest()
        User.objects.create(username=username, password=password, gender=gender)

        return redirect("/manager/user/")


# 删除用户
def manager_user_delete(request):
    del_id = request.GET.get("del_id")
    User.objects.filter(id=del_id).delete()
    return redirect("/manager/user/")


# 更新用户
def manager_user_update(request):
    if request.method == "GET":
        update_id = request.GET.get("update_id")
        user = User.objects.get(id=update_id)
        return render(request, "manager/user_update.html", {"user": user})
    elif request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        # 密码是否更新是可选的，这里只在提供了新密码时更新
        new_password = request.POST.get("password")
        gender = request.POST.get("gender")

        # 更新用户信息
        user = User.objects.get(id=user_id)
        user.username = username
        if new_password:  # 如果提供了新密码
            res = new_password + settings.SECRET_KEY
            password = hashlib.md5(res.encode("utf-8")).hexdigest()
            user.password = password
        user.gender = gender
        user.save()

        return redirect("/manager/user/")


# 评论-------------------------------------------------------------

# 显示所有评论
def manager_review(request):
    if request.method == "GET":
        review_list = Review.objects.select_related('user', 'movie').all()
        return render(request, "manager/review.html", {"review_list": review_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        review_list = Review.objects.filter(
            Q(user__username__icontains=search_query)|
            Q(movie__moviename__icontains=search_query) |
            Q(comment__icontains=search_query) |
            Q(rating__icontains=search_query))
        return render(request, 'manager/review.html', {'review_list': review_list, "search_query": search_query})

# 添加评论
def manager_review_add(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        users = User.objects.all()
        return render(request, "manager/review_add.html", {"movies": movies, "users": users})
    elif request.method == "POST":
        user_id = request.POST.get("user")
        movie_id = request.POST.get("movie")
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        user = User.objects.get(id=user_id)
        movie = Movie.objects.get(id=movie_id)
        Review.objects.create(user=user, movie=movie, comment=comment, rating=rating)
        return redirect("/manager/review/")


# 删除评论
def manager_review_delete(request):
    del_id = request.GET.get("del_id")
    Review.objects.filter(id=del_id).delete()
    return redirect("/manager/review/")


# 更新评论
def manager_review_update(request):
    if request.method == "GET":
        update_id = request.GET.get("update_id")
        review = Review.objects.get(id=update_id)
        movies = Movie.objects.all()
        users = User.objects.all()
        return render(request, "manager/review_update.html", {"review": review, "movies": movies, "users": users})
    elif request.method == "POST":
        review_id = request.POST.get("review_id")
        user_id = request.POST.get("user")
        movie_id = request.POST.get("movie")
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        Review.objects.filter(id=review_id).update(user_id=user_id, movie_id=movie_id, comment=comment, rating=rating)
        return redirect("/manager/review/")

# 收藏------------------------------------------------------------------------

def manager_like(request):
    if request.method == "GET":
        like_list = Like.objects.all()
        return render(request, "manager/like.html", {"like_list": like_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        like_list = Like.objects.filter(
            Q(user__username__icontains=search_query)|
            Q(movie__moviename__icontains=search_query))
        return render(request, 'manager/like.html', {'like_list': like_list, "search_query": search_query})


def manager_like_add(request):
    if request.method == "GET":
        users = User.objects.all()
        movies = Movie.objects.all()
        return render(request, "manager/like_add.html", {"users": users, "movies": movies})
    elif request.method == "POST":
        user_id = request.POST.get("user")
        movie_id = request.POST.get("movie")
        user = User.objects.get(id=user_id)
        movie = Movie.objects.get(id=movie_id)
        Like.objects.create(user=user, movie=movie)
        return redirect("/manager/like/")


def manager_like_delete(request):
    del_id = request.GET.get("del_id")
    like = Like.objects.filter(id=del_id).first()
    if like:
        like.delete()
    return redirect("/manager/like/")

#演员--------------------------------------------------------------
def manager_actor(request):
    if request.method == "GET":
        actor_list = Actor.objects.all()
        return render(request, "manager/actor.html", {"actor_list": actor_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        actor_list = Actor.objects.filter(
            Q(actorname__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(birthday__icontains=search_query) |
            Q(nationality__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
        return render(request, 'manager/actor.html', {'actor_list': actor_list, "search_query": search_query})


# Add Actor
def manager_actor_add(request):
    if request.method == "GET":
        return render(request, "manager/actor_add.html")
    elif request.method == "POST":
        actorname = request.POST.get("actorname")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthday")
        nationality = request.POST.get("nationality")
        bio = request.POST.get("bio")

        try:
            photo = request.FILES['photo']
        except KeyError:
            photo = None

        Actor.objects.create(
            actorname=actorname,
            gender=gender,
            birthday=birthday,
            nationality=nationality,
            bio=bio,
            photo=photo
        )

        return redirect("/manager/actor/")


# Delete Actor
def manager_actor_delete(request):
    del_id = request.GET.get("del_id")
    try:
        actor = Actor.objects.get(id=del_id)
        actor.delete()
    except ObjectDoesNotExist:
        pass

    return redirect("/manager/actor/")


# Update Actor
def manager_actor_update(request):
    if request.method == "GET":
        update_id = request.GET.get("update_id")
        actor = Actor.objects.get(id=update_id)
        return render(request, "manager/actor_update.html", {"actor": actor, "update_id": update_id})
    elif request.method == "POST":
        update_id = request.POST.get("update_id")
        actor = Actor.objects.get(id=update_id)

        actor.actorname = request.POST.get("actorname")
        actor.gender = request.POST.get("gender")
        actor.birthday = request.POST.get("birthday")
        actor.nationality = request.POST.get("nationality")
        actor.bio = request.POST.get("bio")

        try:
            photo = request.FILES['photo']
            actor.photo = photo
        except KeyError:
            pass

        actor.save()

        return redirect("/manager/actor/")


# Cast List and Search
def manager_cast(request):
    if request.method == "GET":
        cast_list = Cast.objects.select_related('movie', 'actor').all()
        return render(request, "manager/cast.html", {"cast_list": cast_list})
    if request.method == "POST":
        search_query = request.POST.get('search')
        cast_list = Cast.objects.filter(
            Q(movie__moviename__icontains=search_query) |
            Q(actor__actorname__icontains=search_query)
        )
        return render(request, 'manager/cast.html', {'cast_list': cast_list, "search_query": search_query})


# Add Cast

def manager_cast_add(request):
    if request.method == "GET":
        # Assume you're passing the actors and movies to the template
        actors = Actor.objects.all()
        movies = Movie.objects.all()
        context = {'actors': actors, 'movies': movies}
        return render(request, "manager/cast_add.html", context)
    elif request.method == "POST":
        movie_id = request.POST.get("movie")
        actor_id = request.POST.get("actor")

        # You can add additional logic here if needed

        # Create a new entry in the Cast model
        Cast.objects.create(
            movie_id=movie_id,
            actor_id=actor_id
        )

        return redirect("/manager/cast/")



# Delete Cast
def manager_cast_delete(request):
    del_id = request.GET.get("del_id")
    try:
        cast = Cast.objects.get(id=del_id)
        cast.delete()
    except ObjectDoesNotExist:
        pass

    return redirect("/manager/cast/")

