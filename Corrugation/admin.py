from django.contrib import admin
from .models import (PaperReels, Product, Partition, PurchaseOrder, Dispatch,
                     Program, Production, ProductionReels, Stock)


class PartitionInline(admin.StackedInline):
    model = Partition


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        PartitionInline,
    ]


admin.site.register(Product, ProductAdmin)


class ProductionReelsInline(admin.StackedInline):
    model = ProductionReels


class ProductionAdmin(admin.ModelAdmin):
    inlines = [
        ProductionReelsInline,
    ]


admin.site.register(Production, ProductionAdmin)
admin.site.register(PaperReels)
admin.site.register(PurchaseOrder)
admin.site.register(Dispatch)
admin.site.register(Program)
admin.site.register(Stock)
