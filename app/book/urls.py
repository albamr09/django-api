from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('authors', views.AuthorViewSet)

app_name = 'book'

urlpatterns = [
    path('', include(router.urls))
]
