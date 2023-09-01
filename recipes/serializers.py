from rest_framework import serializers
from django.contrib.auth.models import User

from tag.models import Tag
from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public',
            'preparation', 'category', 'author', 'tags',
            'tags_objects', 'tags_links',
        ]

    public = serializers.BooleanField(
        source="is_published",
        read_only=True)
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )

    tags_objects = TagSerializer(
        source='tags',
        many=True,
        read_only=True
    )
    tags_links = serializers.HyperlinkedRelatedField(
        view_name="recipes:recipe_api_v2_tag",
        source="tags",
        many=True,
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
