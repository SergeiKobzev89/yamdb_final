from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        lookup_field = "username"
        lookup_value_regex = "[^/]+"


class UserSerializerForUser(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',)
        model = User
        lookup_field = "username"
        lookup_value_regex = "[^/]+"


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField()


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
        required=False
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
        required=False
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        read_only_fields = ['rating']

    def get_rating(self, obj):
        """Получаем среднюю оценку произведения по оценкам пользователей."""
        try:
            rating = obj.reviews.aggregate(Avg('score'))
            return rating.get('score__avg')
        except TypeError:
            return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (request.method != 'PATCH'
            and Review.objects.filter(
                title=title,
                author=request.user).exists()):
            raise serializers.ValidationError('Score already exists')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
        model = Comment
