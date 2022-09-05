from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
)
from users.models import CustomUser, Follow
from .mixins import FollowMixin


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            },
        }


class CustomUserSerializer(UserSerializer, FollowMixin):
    """Сериализатор обработки данных пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class RecipeItemSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных карточки рецепта."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer, FollowMixin):
    """Сериализатор обработки данных о подписке пользователя."""

    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    email = serializers.ReadOnlyField(source='author.email')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    @staticmethod
    def get_recipes_count(obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            queryset = queryset[: int(recipes_limit)]
        return RecipeItemSerializer(queryset, many=True).data

    class Meta:
        model = Follow
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных тега."""

    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeCreateIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор создания ингредиента рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField()

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise exceptions.ValidationError(
                'Нельзя просто так взять и приготовить рецепт без ингредиентов.'
            )
        return value

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных ингредиента в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name',
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=('recipe', 'ingredient'),
            )
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""

    author = CustomUserSerializer(read_only=True)
    name = serializers.CharField(max_length=200)
    image = Base64ImageField()
    ingredients = RecipeCreateIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    cooking_time = serializers.IntegerField()

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def vaildate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиенты должны быть уникальными.'}
                )
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    {
                        'amount': 'Количество ингредиента должно быть больше нуля.'
                    }
                )
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Необходимо выбрать хотя бы один тег.'}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationErro(
                    {'tags': 'Теги должны быть уникальными.'}
                )
            tags_list.append(tag)
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {
                    'cooking_time': 'Время приготовления должно быть больше нуля.'
                }
            )
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self.create_tags(validated_data.pop('tags'), recipe)
        self.create_ingredients(validated_data.pop('ingredients'), recipe)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(recipe, context=context).data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name', 'text'),
                message='Рецепт с таким описанием уже есть в базе.',
            )
        ]


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор отображения рецепта."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        source='recipe_ingredient',
        many=True,
    )
    tags = TagSerializer(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()
    is_cart = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorite',
            'is_cart',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных списка избранного."""

    id = serializers.CharField(read_only=True, source='recipe.id')
    name = serializers.CharField(read_only=True, source='recipe.name')
    image = serializers.CharField(read_only=True, source='recipe.image')
    cooking_time = serializers.CharField(
        read_only=True, source='recipe.cooking_time'
    )

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if user == recipe.author:
            raise serializers.ValidationError(
                {
                    'recipes': 'Нельзя просто так взять и подписаться на свой рецепт.'
                }
            )
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {'recipes': 'Рецепт уже добавлен в избранное.'}
            )
        return data

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор обработки данных списка покупок."""

    id = serializers.CharField(read_only=True, source='recipe.id')
    name = serializers.CharField(read_only=True, source='recipe.name')
    image = serializers.CharField(read_only=True, source='recipe.image')
    cooking_time = serializers.CharField(
        read_only=True, source='recipe.cooking_time'
    )

    class Meta:
        model = Cart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
