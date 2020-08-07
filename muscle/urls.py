from django.urls import path, include
from django.contrib import admin
from . import views

app_name='muscle'

urlpatterns=[
        path('', views.index, name='index'),
        path('<int:year>/<int:month>/<int:span>',views.index,name='index'),
]