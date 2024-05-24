from django.urls import path
from .views import (index, paper_reels, update_reel, delete_reel,
                    add_purchase_order_detail, add_product, add_dispatch,
                    purchase_order, add_purchase_order_detailed,
                    delete_purchase_order, daily_program)

app_name = 'Corrugation'

urlpatterns = [
    path('', index, name='index'),
    path('paper_reels/', paper_reels, name='paper_reels'),
    path('update-reel/<int:pk>/', update_reel, name='update_reel'),
    path('delete-reel/<int:pk>/', delete_reel, name='delete_reel'),
    path('purchase-order/', purchase_order, name='purchase_order'),
    path('add-purchase-order-detail/', add_purchase_order_detail, name='add_purchase_order_detail'),
    path('add-purchase-order-detailed/', add_purchase_order_detailed, name='add_purchase_order_detailed'),
    path('add-product/', add_product, name='add_product'),
    path('add-dispatch/', add_dispatch, name='add_dispatch'),
    path('delete-purchase-order/<int:pk>/', delete_purchase_order, name='delete_purchase_order'),
    path('program/', daily_program, name='program'),
]
