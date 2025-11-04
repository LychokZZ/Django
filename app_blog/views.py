from django.shortcuts import render
from django.views.generic import TemplateView
from app_blog.models import Article

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        articles = (
            Article.objects
            .select_related('category')
            .prefetch_related('images')
            .order_by('-pub_date')
        )
        return render(request, self.template_name, {'articles': articles})
