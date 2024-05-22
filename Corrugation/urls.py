from django.urls import path
from .views import paper_reels, index

app_name = 'Corrugation'

urlpatterns = [
    path('', index, name='index'),
    path('paper_reels/', paper_reels, name='paper_reels'),
]
