from django.urls import path

from .views import (file_delete, file_history, file_imports,
                    file_nodes, files_updates)

urlpatterns = [
    path('imports', file_imports),
    path('nodes/<slug:pk>', file_nodes),
    path('delete/<slug:pk>', file_delete),
    path('updates', files_updates),
    path('node/<slug:pk>/history', file_history)
]
