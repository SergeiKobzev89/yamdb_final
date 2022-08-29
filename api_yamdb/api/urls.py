from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, Users, email, token)

app_name = 'api'

router = DefaultRouter()

router.register(r'users', Users, basename='users')
router.register(
    'genres',
    GenreViewSet)
router.register(
    'categories',
    CategoryViewSet)
router.register(
    'titles',
    TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',)

urlpatterns = [
    path('v1/auth/token/', token),
    path('v1/auth/signup/', email),
    path('v1/', include(router.urls)), ]
