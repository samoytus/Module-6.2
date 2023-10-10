from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList

urlpatterns = [
   path('', ProductsList.as_view()),
]