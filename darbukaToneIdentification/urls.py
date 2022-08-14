from django.contrib import admin
from django.urls import path
from darbukaToneIdentification import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('training/', views.training),
    path('identification/developer', views.developerIdentification),
    path('identification/user', views.userIdentification),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)