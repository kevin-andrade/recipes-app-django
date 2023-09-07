from rest_framework import serializers

from tag.models import Tag
from .models import Recipe
from authors.validators import AuthorRecipeValidator


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit', 'preparation_steps', 'cover'
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

    tag_objects = TagSerializer(
        source='tags',
        many=True,
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        view_name="recipes:recipe_api_v2_tag",
        source="tags",
        many=True,
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate
