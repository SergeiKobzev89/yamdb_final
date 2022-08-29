from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'имя пользователя', max_length=150, unique=True)
    email = models.EmailField('адрес электронной почты', unique=True,
                              db_index=True)
    role = models.CharField('права пользователя',
                            max_length=9, choices=ROLE_CHOICES, default='user')
    bio = models.TextField('коротко о себе', max_length=500, blank=True)
    confirm = models.CharField('код подтверждения', max_length=200, blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ['pk']
        verbose_name = "пользователь"

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Category(models.Model):
    """Описание таблицы категорий произведений."""
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name="Имя категории",
        help_text="Введите имя категории",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Тэг категории",
        help_text="Введите короткий тэг категории",
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Описание таблицы жанров произведений."""
    name = models.CharField(
        max_length=40,
        blank=False,
        null=False,
        verbose_name="Имя жанра",
        help_text="Введите имя жанра",
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Тэг жанра",
        help_text="Введите короткий тэг жанра",
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Описание таблицы произведений."""
    name = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name="Имя произведения",
        help_text="Введите имя произведения",
    )
    year = models.IntegerField(
        blank=False,
        null=False,
        validators=[MaxValueValidator(dt.today().year)],
        verbose_name="Дата создания",
        help_text="Введите год создания произведения, yyyy",
    )
    description = models.TextField(
        blank=True,
        null=True,
        default='',
        verbose_name="Подробности",
        help_text="Подрбности/описание",
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name="title",
        null=True,
        verbose_name="Категория произведения",
    )
    genre = models.ManyToManyField(
        to=Genre,
        related_name="title",
        blank=True,
        verbose_name="Жанры произведения",
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    pub_date = models.DateTimeField(
        'review pub date', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'comment pub date', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text
