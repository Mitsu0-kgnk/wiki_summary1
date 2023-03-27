from django.contrib import admin
from django.urls import path,include
from .views import Form,SummaryView
from . import views


urlpatterns = [
    path('', Form.as_view(), name='index'),
    path('summary/', views.SummaryView.as_view(), name='summary')
]