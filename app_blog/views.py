from django.shortcuts import render
from django.views.generic import ListView, DateDetailView
from .models import Article, Category

class HomePageView(ListView):
    # показуємо категорії + додаємо 5 публікацій на головну
    model = Category                        # ← головний queryset — категорії
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['articles'] = (
            Article.objects
            .filter(main_page=True)
            .select_related('category')
            .prefetch_related('images')
            .order_by('-pub_date')[:5]
        )
        return ctx


class ArticleDetail(DateDetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'item'

    date_field = 'pub_date'      # можна DateTimeField — ок
    month_format = '%m'
    allow_future = True

    slug_field = 'slug'          # ← явні параметри
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # щоб детальна сторінка не робила зайвих запитів
        return (
            Article.objects
            .select_related('category')
            .prefetch_related('images')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # images вже у prefetch, але залишу для зручності використання в шаблоні
        ctx['images'] = ctx['item'].images.all()
        return ctx


class ArticleList(ListView):
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'items'
    paginate_by = 10  # за бажанням

    def get_queryset(self):
        return (
            Article.objects
            .select_related('category')
            .prefetch_related('images')
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        ctx['category'] = Category.objects.filter(slug=slug).first() if slug else None
        return ctx


class ArticleCategoryList(ArticleList):
    def get_queryset(self):
        # простіший фільтр, без __in для одного значення
        return (
            Article.objects
            .filter(category__slug=self.kwargs['slug'])
            .select_related('category')
            .prefetch_related('images')
            .order_by('-pub_date')
        )
