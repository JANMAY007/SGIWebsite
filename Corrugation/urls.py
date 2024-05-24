from django.urls import path
from .views import index, paper_reels, update_reel, delete_reel

app_name = 'Corrugation'

urlpatterns = [
    path('', index, name='index'),
    path('paper_reels/', paper_reels, name='paper_reels'),
    path('update-reel/<int:pk>/', update_reel, name='update_reel'),
    path('delete-reel/<int:pk>/', delete_reel, name='delete_reel'),
]
