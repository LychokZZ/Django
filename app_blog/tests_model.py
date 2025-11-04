from django.test import TestCase
from django.db.utils import IntegrityError
from app_blog.models import Category

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='Innovations', slug='innovations')
