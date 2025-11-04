# -*- coding: utf-8 -*-
from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Article, ArticleImage, Category
from .forms import ArticleImageForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}  # автозаповнення slug з назви категорії
    fieldsets = (
        (None, {'fields': ('category', 'slug')}),
    )

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    form = ArticleImageForm
    extra = 0
    fieldsets = (
        (None, {'fields': ('title', 'image')}),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'slug', 'main_page')
    inlines = [ArticleImageInline]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category',)
    fieldsets = (
        (None, {'fields': ('pub_date', 'title', 'description', 'main_page', 'category')}),
        ('Додатково', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': ('slug',),
        }),
    )

    def delete_file(self, pk, request):
        obj = get_object_or_404(ArticleImage, pk=pk)
        return obj.delete()
