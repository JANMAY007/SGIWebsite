from django.contrib import admin
from .models import PaperReels, Product, PurchaseOrder, Dispatch


admin.site.register(PaperReels)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(Dispatch)
