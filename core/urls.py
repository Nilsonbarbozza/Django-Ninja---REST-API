from django.contrib import admin
from django.urls import path
from .api import api #tenho que criar o arquivo api.py necessario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls) #Primeiro passo para criar a Router- url/ + api.urls
]

