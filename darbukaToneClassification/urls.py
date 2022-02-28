from django.contrib import admin
from django.urls import path
from darbukaToneClassification import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('training/', views.training),
    path('basic-tone/', views.basicTone),
]
