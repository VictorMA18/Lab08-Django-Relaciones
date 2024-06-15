from django.urls import path
from . import views

urlpatterns = [
    path('generar_pdf/', views.GeneratePDF.as_view(), name='generar_pdf'),
]