from django.urls import path
from . import views, apps

app_name = apps.BackendConfig.name
urlpatterns = [
    path('process-query', views.process_query),
    path('make-csv', views.csv_request),
]
