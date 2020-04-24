from django.urls import path
from . import views, apps

app_name = apps.BackendConfig.name
urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.results, name='results'),
]
