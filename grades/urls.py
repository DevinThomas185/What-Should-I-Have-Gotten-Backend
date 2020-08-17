from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<path:details>', views.grades, name='grades')
]