from django.urls import path

from .views import index_controller

urlpatterns = [
    path("", index_controller),
]
