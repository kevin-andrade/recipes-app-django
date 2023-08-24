from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'created_at', 'is_published']
    list_display_links = ['title', 'description']
    list_editable = ['is_published']
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html'
    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }
    autocomplete_fields = 'tags',
