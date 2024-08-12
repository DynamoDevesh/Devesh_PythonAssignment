from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),  # Root path redirects to upload file
    path('upload/', views.upload_file, name='upload_file'),
    path('pdf_summary/', views.pdf_summary, name='pdf_summary'),
]
