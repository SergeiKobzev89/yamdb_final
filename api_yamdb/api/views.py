from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsOwner,
                          ReviewCommentPermissions)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmSerializer, EmailSerializer, GenreSerializer,
                          ReviewSerializer, TitleReadSerializer,
                          TitleSerializer, UserSerializer,
                          UserSerializerForUser)

FORBIDDEN_USERNAMES = ['me', ]


class Users(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = "[^/]+"

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[
            IsAuthenticated,
            IsOwner, ])
    def me(self, request):
        self.kwargs['username'] = request.user.username

        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            # if not request.user.is_admin:
            return self.partial_update(request)
        else:
            raise Exception('Not implemented')

    def get_serializer_class(self):
        if self.request.user.role == User.USER:
            return UserSerializerForUser
        return UserSerializer


def send_msg(email, confirmation_code):
    subject = "Confirmation code"
    body = f"Ваш код подтверждения: {confirmation_code}"
    send_mail(
        subject, body, None, [email, ],
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mail = serializer.data.get('email')
    username = serializer.data.get('username')
    if username in FORBIDDEN_USERNAMES:
        return Response(
            {'username': f'Wrong username. {username} запрешен'},
            status=status.HTTP_400_BAD_REQUEST)
    confirm = get_random_secret_key()
    if User.objects.filter(username=username).exists():
        return Response(
            {'username': f'Wrong username. Уже есть  - {username} '},
            status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=mail).exists():
        return Response(
            {'email': f'Wrong email. Почтовый адрес - {mail}  - уже есть'},
            status=status.HTTP_400_BAD_REQUEST)
    User.objects.create(
        email=mail,
        username=username,
        confirm=confirm
    )
    send_msg(mail, confirm)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    user = get_object_or_404(User, username=username)
    if user.confirm == serializer.data.get('confirmation_code'):
        token = str(RefreshToken.for_user(user).access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Wrong confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)


class CreateListDestroyViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               ):
    """ViewSet обрабатывает создание, просмотр всех и удаление.
    Поиск и фильтрация по полям name, slug.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = TitleFilter
    search_fields = ('name', )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermissions, IsAuthenticatedOrReadOnly)

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        context.update({'title': title})
        return context

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)
