from django.urls import path
from .views import *

urlpatterns = [
    path('', InicioView.as_view(), name='index'),
    # path('detalle/<str:id>/', Detalles.as_view(), name='detalles'),
]
