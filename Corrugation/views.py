from calendar import month_abbr
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect, get_object_or_404
from .models import (PaperReels, Product, Partition, PurchaseOrder, Dispatch,
                     Program, Production, ProductionReels, Stock)


def index(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        stock_quantity = request.POST.get('stock_quantity')
        try:
            stock_quantity = int(stock_quantity)
            product = Product.objects.get(product_name=product_name)
            stock, created = Stock.objects.get_or_create(product=product)
            stock.stock_quantity = stock_quantity
            stock.save()
        except (ValueError, TypeError):
            pass
        return redirect('Corrugation:index')
    context = {
        'products': Product.objects.all().values('product_name'),
        'stocks': Stock.objects.all().values('product__product_name', 'stock_quantity'),
    }
    return render(request, 'index.html', context)


def search_reels(request):
    query = request.GET.get('q', '')
    if query:
        results = PaperReels.objects.filter(
            Q(reel_number__icontains=query) |
            Q(bf__icontains=query) |
            Q(gsm__icontains=query) |
            Q(size__icontains=query) |
            Q(weight__icontains=query)
        )
        results_data = [
            {
                'reel_number': reel.reel_number,
                'bf': reel.bf,
                'gsm': reel.gsm,
                'size': reel.size,
                'weight': reel.weight,
            }
            for reel in results
        ]
    else:
        results_data = []
    return JsonResponse({'results': results_data})


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
        reel.used = True
        reel.save()
        return redirect('Corrugation:paper_reels')
    return redirect('Corrugation:paper_reels')


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        box_no = request.POST.get('box_no')
        material_code = request.POST.get('material_code')
        size = request.POST.get('size')
        inner_length = request.POST.get('inner_length', None)
        inner_breadth = request.POST.get('inner_breadth', None)
        inner_depth = request.POST.get('inner_depth', None)
        outer_length = request.POST.get('outer_length', None)
        outer_breadth = request.POST.get('outer_breadth', None)
        outer_depth = request.POST.get('outer_depth', None)
        color = request.POST.get('color', '')
        weight = request.POST.get('weight', None)
        ply = request.POST.get('ply', None)
        gsm = request.POST.get('gsm', None)
        bf = request.POST.get('bf', None)
        cs = request.POST.get('cs', None)
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
            color=color,
            weight=weight,
            ply=ply,
            gsm=gsm,
            bf=bf,
            cs=cs
        )

        partition_data = zip(
            request.POST.getlist('partition_size'),
            request.POST.getlist('partition_od'),
            request.POST.getlist('deckle_cut'),
            request.POST.getlist('length_cut'),
            request.POST.getlist('partition_type'),
            request.POST.getlist('ply_no'),
            request.POST.getlist('partition_weight'),
            request.POST.getlist('partition_gsm'),
            request.POST.getlist('partition_bf')
        )

        for partition in partition_data:
            Partition.objects.create(
                product_name=product,
                partition_size=partition[0],
                partition_od=partition[1],
                deckle_cut=partition[2],
                length_cut=partition[3],
                partition_type=partition[4],
                ply_no=partition[5],
                partition_weight=partition[6],
                gsm=partition[7],
                bf=partition[8]
            )
        return redirect('Corrugation:add_product')
    context = {
        'products': Product.objects.all().values('product_name', 'pk'),
    }
    return render(request, 'products.html', context)


def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    partitions = Partition.objects.filter(product_name=product)
    context = {
        'product': product,
        'partitions': partitions
    }
    return render(request, 'product_detail.html', context)


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
        for po in purchase_orders:
            total_dispatch_quantity = sum(dispatch.dispatch_quantity for dispatch in po.dispatches)
            po.remaining_quantity = po.po_quantity - total_dispatch_quantity
            po.max_remaining_quantity = po.po_quantity + (po.po_quantity * 5 / 100) - total_dispatch_quantity
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
        pk = request.POST.get('pk')
        po = get_object_or_404(PurchaseOrder, id=pk)
        dispatch_date = request.POST['dispatch_date']
        dispatch_quantity = request.POST['dispatch_quantity']

        Dispatch.objects.create(
            po=po,
            dispatch_date=dispatch_date,
            dispatch_quantity=dispatch_quantity
        )
        # remove dispatch quantity from stock of particular product
        stock = Stock.objects.get(product=po.product_name)
        stock.stock_quantity -= int(dispatch_quantity)
        stock.save()
        return redirect('Corrugation:purchase_order')
    return redirect('Corrugation:purchase_order')


def daily_program(request):
    if request.method == 'POST':
        # Extract data from POST request
        data = request.POST
        product_name = data.get('product_name')
        program_quantity = data.get('program_quantity')
        program_date_str = data.get('program_date')
        program_notes = data.get('program_notes')
        # Convert program_date from string to datetime
        program_date = datetime.strptime(program_date_str, '%Y-%m-%d').date()
        # Create a new Program instance
        Program.objects.create(
            product=Product.objects.get(product_name=product_name),
            program_quantity=program_quantity,
            program_date=program_date,
            program_notes=program_notes
        )
        return redirect('Corrugation:daily_program')
    programs = Program.objects.filter(active=True)
    # Prepare data to return
    programs_data = []
    for program in programs:
        # Get related product
        product = program.product

        # Get related partitions for the product
        partitions = Partition.objects.filter(product_name=product)

        # Prepare partition data
        partitions_data = []
        for partition in partitions:
            partition_data = {
                'partition_size': partition.partition_size,
                'partition_od': partition.partition_od,
                'deckle_cut': partition.deckle_cut,
                'length_cut': partition.length_cut,
                'partition_type': partition.get_partition_type_display(),
                'ply_no': partition.get_ply_no_display(),
                'partition_weight': partition.partition_weight
            }
            partitions_data.append(partition_data)

        # Prepare program data
        program_data = {
            'product_name': product.product_name,
            'box_no': product.box_no,
            'material_code': product.material_code,
            'size': product.size,
            'inner_length': product.inner_length,
            'inner_breadth': product.inner_breadth,
            'inner_depth': product.inner_depth,
            'outer_length': product.outer_length,
            'outer_breadth': product.outer_breadth,
            'outer_depth': product.outer_depth,
            'gsm': product.gsm,
            'bf': product.bf,
            'color': product.color,
            'weight': product.weight,
            'partitions': partitions_data,
            'program_quantity': program.program_quantity,
            'program_date': program.program_date.strftime('%Y-%m-%d'),
            'program_notes': program.program_notes,
        }
        programs_data.append(program_data)
    context = {
        'programs': programs_data,
        'products': Product.objects.all().values('product_name'),
    }
    return render(request, 'program.html', context)


def production(request):
    if request.method == 'POST':
        # Extract data from POST request
        data = request.POST
        product_name = data.get('product')
        reel_numbers = data.getlist('reels')  # getlist to handle multiple reels
        production_quantity = data.get('production_quantity')

        # Create a new Production instance
        product_instance = Product.objects.get(product_name=product_name)
        production_object = Production.objects.create(
            product=product_instance,
            production_quantity=production_quantity,
            production_date=timezone.now(),
        )
        stock, create = Stock.objects.get_or_create(product=product_instance)
        stock.stock_quantity += int(production_quantity)
        stock.save()
        # Create new ProductionReels instances for each reel number
        for reel_number in reel_numbers:
            reel_instance = PaperReels.objects.get(reel_number=reel_number)
            ProductionReels.objects.create(
                production=production_object,
                reel=reel_instance,
            )
        return redirect('Corrugation:production')

    production_objects = Production.objects.filter(active=True)
    production_data = []
    for production_object in production_objects:
        production_reels = ProductionReels.objects.filter(production=production_object)
        reels_data = [reel.reel.reel_number for reel in production_reels]
        production_data.append({
            'pk': production_object.pk,
            'product_name': production_object.product.product_name,
            'production_quantity': production_object.production_quantity,
            'production_date': production_object.production_date,
            'reels': reels_data,
        })

    context = {
        'products': Product.objects.all().values('product_name'),
        'reels': PaperReels.objects.all().values('reel_number'),
        'productions': production_data,
    }
    return render(request, 'production.html', context)


def update_production_quantity(request):
    if request.method == 'POST':
        production_object = get_object_or_404(Production, pk=request.POST.get('pk'))
        product = Product.objects.get(product_name=production_object.product.product_name)
        stock, created = Stock.objects.get_or_create(product=product)
        stock.stock_quantity -= int(production_object.production_quantity)
        production_object.production_quantity = request.POST.get('production_quantity')
        production_object.save()
        stock.stock_quantity += int(production_object.production_quantity)
        stock.save()
        return redirect('Corrugation:production')
    return redirect('Corrugation:production')


def add_reel_to_production(request):
    if request.method == 'POST':
        production_object = get_object_or_404(Production, pk=request.POST.get('pk'))
        reel_number = request.POST.get('reel_number')
        try:
            reel = PaperReels.objects.get(reel_number=reel_number)
            ProductionReels.objects.create(production=production_object, reel=reel)
        except PaperReels.DoesNotExist:
            # Optionally handle the error if reel does not exist
            pass
        return redirect('Corrugation:production')
    return redirect('Corrugation:production')


def delete_production(request):
    if request.method == 'POST':
        production_object = get_object_or_404(Production, pk=request.POST.get('pk'))
        # delete reels that are used in production
        used_reels = ProductionReels.objects.filter(production=production_object)
        for reel in used_reels:
            PaperReels.objects.get(reel_number=reel.reel.reel_number).used = True
        ProductionReels.objects.filter(production=production_object).delete()
        production_object.active = False
        production_object.save()
        return redirect('Corrugation:production')
    return redirect('Corrugation:production')
