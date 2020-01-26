# api/urls.py

from django.urls import path, re_path
from django.conf.urls import url
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('<int:id>', views.document),
    path('health', views.health_check),
]