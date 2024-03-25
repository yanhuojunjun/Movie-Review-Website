from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=32, unique=False)
    gender = models.CharField(max_length=10)

    class Meta:
        db_table = "User"


class Director(models.Model):
    directorname = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    birthday = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        db_table = "Director"



class Movie(models.Model):
    moviename = models.CharField(max_length=100)
    director = models.ForeignKey(to="Director", to_field="id", on_delete=models.CASCADE)
    type = models.CharField(max_length=40)
    time = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    length = models.IntegerField()
    web = models.URLField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        db_table = "Movie"


class Like(models.Model):
    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, to_field="id", on_delete=models.CASCADE)

    class Meta:
        db_table = "Like"
        unique_together = ('user', 'movie')


class Review(models.Model):
    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, to_field="id", on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # 限制评分在 1 到 5 之间
        null=True, blank=True)

    class Meta:
        db_table = "Review"
        unique_together = ('user', 'movie')


class Actor(models.Model):
    actorname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        db_table = "Actor"


class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    class Meta:
        db_table = "Cast"
        unique_together = ('movie', 'actor')
