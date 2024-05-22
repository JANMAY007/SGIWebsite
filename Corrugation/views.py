from django.shortcuts import render, redirect
from .models import PaperReels, Product, PurchaseOrder, Dispatch


def index(request):
    return render(request, 'index.html')


def paper_reels(request):
    if request.method == 'POST':
        reel_number = request.POST.get('reel_number')
        bf = request.POST.get('bf')
        gsm = request.POST.get('gsm')
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        try:
            bf = int(bf)
            gsm = int(gsm)
            size = int(size)
            weight = int(weight)
            PaperReels.objects.create(
                reel_number=reel_number,
                bf=bf,
                gsm=gsm,
                size=size,
                weight=weight
            )
            return redirect('Corrugation:paper_reels')
        except (ValueError, TypeError):
            return render(request, 'paper_reel.html', {'error': 'Invalid input. Please enter valid numbers.'})
    reels = PaperReels.objects.all()
    context = {
        'reels': reels,
    }
    return render(request, 'paper_reel.html', context)


def products(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        box_no = request.POST.get('box_no')
        material_code = request.POST.get('material_code')
        size = request.POST.get('size')
        inner_length = request.POST.get('inner_length')
        inner_breadth = request.POST.get('inner_breadth')
        inner_depth = request.POST.get('inner_depth')
        outer_length = request.POST.get('outer_length')
        outer_breadth = request.POST.get('outer_breadth')
        outer_depth = request.POST.get('outer_depth')
        box = request.POST.get('box')
        color = request.POST.get('color')
        weight = request.POST.get('weight')
        partition_size = request.POST.get('partition_size')
        partition_od = request.POST.get('partition_od')
        deckle_cut = request.POST.get('deckle_cut')
        length_cut = request.POST.get('length_cut')
        partition_type = request.POST.get('partition_type')
        ply_no = request.POST.get('ply_no')
        partition_weight = request.POST.get('partition_weight')
        Product.objects.create(product_name=product_name, box_no=box_no, material_code=material_code, size=size,
                               inner_length=inner_length, inner_breadth=inner_breadth, inner_depth=inner_depth,
                               outer_length=outer_length, outer_breadth=outer_breadth, outer_depth=outer_depth,
                               box=box, color=color, weight=weight, partition_size=partition_size,
                               partition_od=partition_od, deckle_cut=deckle_cut, length_cut=length_cut,
                               partition_type=partition_type, ply_no=ply_no, partition_weight=partition_weight)
    product = Product.objects.all()
    context = {
        'products': product,
    }
    return render(request, 'products.html', context)


def purchase_order(request):
    if request.method == 'POST':
        po_number = request.POST.get('po_number')
        po_date = request.POST.get('po_date')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        PurchaseOrder.objects.create(po_number=po_number, po_date=po_date, product=product, quantity=quantity)
    purchase_orders = PurchaseOrder.objects.all()
    dispatches = Dispatch.objects.filter(po__in=[po.po_number for po in purchase_orders])
    context = {
        'purchase_orders': purchase_orders,
        'dispatches': dispatches,
    }
    return render(request, 'purchase_order.html', context)


def dispatch(request):
    if request.method == 'POST':
        po = request.POST.get('po')
        dispatch_date = request.POST.get('dispatch_date')
        dispatch_quantity = request.POST.get('dispatch_quantity')
        Dispatch.objects.create(po=po, dispatch_date=dispatch_date, dispatch_quantity=dispatch_quantity)
        return render(request, 'dispatch.html', {'dispatches': Dispatch.objects.all()})
    dispatches = Dispatch.objects.all()
    return render(request, 'dispatch.html', {'dispatches': dispatches})
