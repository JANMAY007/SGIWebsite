from django.db import models


class PaperReels(models.Model):
    class Meta:
        verbose_name = 'Paper Reel'
        verbose_name_plural = 'Paper Reels'
    reel_number = models.CharField(max_length=10)
    bf = models.PositiveSmallIntegerField(default=18)
    gsm = models.PositiveSmallIntegerField(default=120)
    size = models.PositiveSmallIntegerField(default=41)
    weight = models.PositiveSmallIntegerField(default=545)
    object = models.manager

    def __str__(self):
        return f'{self.reel_number}'


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    product_name = models.CharField(max_length=100, unique=True)
    box_no = models.CharField(max_length=8)
    material_code = models.CharField(max_length=10)
    size = models.CharField(max_length=10)  # change this
    inner_length = models.PositiveSmallIntegerField()
    inner_breadth = models.PositiveSmallIntegerField()
    inner_depth = models.PositiveSmallIntegerField()
    outer_length = models.PositiveSmallIntegerField()
    outer_breadth = models.PositiveSmallIntegerField()
    outer_depth = models.PositiveSmallIntegerField()
    box = models.CharField(max_length=20)  # check this
    color = models.CharField(max_length=20)
    weight = models.CharField(max_length=7)
    partition_size = models.CharField(max_length=10)  # change this
    partition_od = models.CharField(max_length=50)
    deckle_cut = models.CharField(max_length=1)
    length_cut = models.CharField(max_length=1)
    partition_type_choice = (
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('z-type', 'Z-Type'),
    )
    partition_type = models.CharField(max_length=10, choices=partition_type_choice)
    ply_no_choices = (
        ('3', '3 Ply'),
        ('5', '5 Ply'),
        ('7', '7 Ply'),
    )
    ply_no = models.CharField(max_length=1, choices=ply_no_choices)
    partition_weight = models.CharField(max_length=7)
    objects = models.manager

    def __str__(self):
        return f'{self.product_name} - {self.box_no}'


class PurchaseOrder(models.Model):
    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=10)
    po_date = models.DateField()
    rate = models.FloatField()
    po_quantity = models.PositiveIntegerField()
    objects = models.manager

    def __str__(self):
        return f'{self.product_name} - {self.po_date} - {self.po_number}'


class Dispatch(models.Model):
    class Meta:
        verbose_name = 'Dispatch'
        verbose_name_plural = 'Dispatches'
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    dispatch_date = models.DateField()
    dispatch_quantity = models.PositiveIntegerField()
    objects = models.manager

    def __str__(self):
        return f'{self.po} - {self.dispatch_date}'
