from django.urls import path
from .views import file_imports, files_nodes, file_nodes, file_delete

urlpatterns = [
    path('imports/', file_imports),
    path('nodes/', files_nodes),
    path('nodes/<slug:pk>/', file_nodes),
    path('delete/<slug:pk>/', file_delete)
]
