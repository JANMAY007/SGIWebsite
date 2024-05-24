from calendar import month_abbr
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect, get_object_or_404
from .models import PaperReels, Product, Partition, PurchaseOrder, Dispatch


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


def update_reel(request, pk):
    reel = get_object_or_404(PaperReels, pk=pk)
    if request.method == 'POST':
        reel.reel_number = request.POST.get('reel_number')
        reel.bf = request.POST.get('bf')
        reel.gsm = request.POST.get('gsm')
        reel.size = request.POST.get('size')
        reel.weight = request.POST.get('weight')
        reel.save()
        return redirect('Corrugation:paper_reels')
    return redirect('Corrugation:paper_reels')


def delete_reel(request, pk):
    reel = get_object_or_404(PaperReels, pk=pk)
    if request.method == 'POST':
        reel.delete()
        return redirect('Corrugation:paper_reels')
    return redirect('Corrugation:paper_reels')


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        box_no = request.POST['box_no']
        material_code = request.POST['material_code']
        size = request.POST['size']
        inner_length = request.POST['inner_length']
        inner_breadth = request.POST['inner_breadth']
        inner_depth = request.POST['inner_depth']
        outer_length = request.POST['outer_length']
        outer_breadth = request.POST['outer_breadth']
        outer_depth = request.POST['outer_depth']
        box = request.POST['box']
        color = request.POST['color']
        weight = request.POST['weight']

        product = Product.objects.create(
            product_name=product_name,
            box_no=box_no,
            material_code=material_code,
            size=size,
            inner_length=inner_length,
            inner_breadth=inner_breadth,
            inner_depth=inner_depth,
            outer_length=outer_length,
            outer_breadth=outer_breadth,
            outer_depth=outer_depth,
            box=box,
            color=color,
            weight=weight
        )

        partition_size = request.POST.getlist('partition_size')
        partition_od = request.POST.getlist('partition_od')
        deckle_cut = request.POST.getlist('deckle_cut')
        length_cut = request.POST.getlist('length_cut')
        partition_type = request.POST.getlist('partition_type')
        ply_no = request.POST.getlist('ply_no')
        partition_weight = request.POST.getlist('partition_weight')

        for i in range(len(partition_size)):
            Partition.objects.create(
                product_name=product,
                partition_size=partition_size[i],
                partition_od=partition_od[i],
                deckle_cut=deckle_cut[i],
                length_cut=length_cut[i],
                partition_type=partition_type[i],
                ply_no=ply_no[i],
                partition_weight=partition_weight[i]
            )
    return redirect('Corrugation:purchase_order')


def purchase_order(request):
    # Get all purchase orders month-wise for each po_given_by
    months_with_counts = PurchaseOrder.objects.filter(active=True).annotate(
        month=ExtractMonth('po_date')
    ).values('month', 'po_given_by', 'product_name__product_name').annotate(
        po_count=Count('id')
    ).order_by('month', 'po_given_by')

    for item in months_with_counts:
        item['month'] = month_abbr[item['month']]

    context = {
        'purchase_order_list': months_with_counts,
        'products': Product.objects.all(),
        'po_given_by_choices': PurchaseOrder.po_given_by_choices,
    }
    return render(request, 'purchase_order.html', context)


def add_purchase_order_detailed(request):
    if request.method == 'POST':
        product_id = request.POST['product_name']
        product = get_object_or_404(Product, id=product_id)
        po_given_by = request.POST['po_given_by']
        po_number = request.POST['po_number']
        po_date = request.POST['po_date']
        rate = request.POST['rate']
        po_quantity = request.POST['po_quantity']

        PurchaseOrder.objects.create(
            product_name=product,
            po_given_by=po_given_by,
            po_number=po_number,
            po_date=po_date,
            rate=rate,
            po_quantity=po_quantity
        )

        return redirect('Corrugation:purchase_order')


def add_purchase_order_detail(request):
    if request.method == 'POST':
        month_word = request.POST['month']
        po_given_by = request.POST['po_given_by']

        # Convert month_word to a numeric month
        month_dict = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }
        month_numeric = month_dict.get(month_word)

        # Get purchase orders for the given month and po_given_by
        purchase_orders = PurchaseOrder.objects.filter(
            po_date__month=month_numeric,
            po_given_by=po_given_by,
            active=True
        ).select_related('product_name')

        # Get dispatches for the selected purchase orders
        purchase_order_ids = purchase_orders.values_list('id', flat=True)
        dispatches = Dispatch.objects.filter(po_id__in=purchase_order_ids).select_related('po')
        # Group dispatches by purchase order
        dispatches_dict = {}
        for dispatch in dispatches:
            if dispatch.po_id not in dispatches_dict:
                dispatches_dict[dispatch.po_id] = []
            dispatches_dict[dispatch.po_id].append(dispatch)

        # Add dispatches to purchase orders
        for po in purchase_orders:
            po.dispatches = dispatches_dict.get(po.id, [])
        context = {
            'purchase_orders': purchase_orders,
        }
        return render(request, 'purchase_order_details.html', context)


def delete_purchase_order(request, pk):
    if request.method == 'POST':
        po = get_object_or_404(PurchaseOrder, pk=pk)
        po.active = False
        po.save()
        return redirect('Corrugation:purchase_order')


def add_dispatch(request):
    if request.method == 'POST':
        po_id = request.POST['po']
        po = get_object_or_404(PurchaseOrder, id=po_id)
        dispatch_date = request.POST['dispatch_date']
        dispatch_quantity = request.POST['dispatch_quantity']

        Dispatch.objects.create(
            po=po,
            dispatch_date=dispatch_date,
            dispatch_quantity=dispatch_quantity
        )

    return redirect('Corrugation:add_purchase_order_detail')
