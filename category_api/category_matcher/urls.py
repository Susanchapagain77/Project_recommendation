from django.urls import path
from .views import match_category

urlpatterns = [
    path('',match_category) 
]
