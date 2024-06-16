from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generar_pdf_basic/', views.get_pdf, name='generar_pdf_basic'),
    path('generar_pdf_advanced/', views.get_pdf_advanced, name='generar_pdf_advanced'),
]