from django.urls import path
from clothes import views

urlpatterns = [
    path('api/clothes/', views.clothes_list),
    path('api/clothes/<int:pk>/', views.clothes_detail),
]