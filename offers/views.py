from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Offer, OfferCounter, DeliveryMethod, Stage, OfferProduct
from company.models import Contact, Company
from .forms import OfferForm, InitializeCounterForm, DeliveryMethodForm, StageForm, OfferProductForm
from django.contrib import messages

def initialize_counter(request):
    if request.method == 'POST':
        form = InitializeCounterForm(request.POST)
        if form.is_valid():
            initial_number = form.cleaned_data['initial_number']
            counter, created = OfferCounter.objects.get_or_create(pk=1)
            counter.base_number = initial_number
            counter.current_number = initial_number
            counter.save()
            messages.success(request, 'Counter initialized successfully.')
            return redirect('offers:list')
    else:
        form = InitializeCounterForm()
    return render(request, 'offers/initialize_counter.html', {'form': form})

def create_offer(request):
    company_id = request.GET.get('company_id')
    initial_data = {}
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        initial_data['company'] = company

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            messages.success(request, 'Offer created successfully.')
            return redirect('offers:offer_detail', pk=offer.pk)
    else:
        form = OfferForm(initial=initial_data)
        
    return render(request, 'offers/create_offer.html', {'form': form})

def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'offers/offer_list.html', {'offers': offers})

def offer_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    offer_products = OfferProduct.objects.filter(offer=offer)
    total_amount = sum(product.total_price() for product in offer_products)
    return render(request, 'offers/offer_detail.html', {'offer': offer, 'offer_products': offer_products, 'total_amount': total_amount})

def load_contacts(request):
    company_id = request.GET.get('company_id')
    contacts = Contact.objects.filter(company_id=company_id).all()
    return JsonResponse(list(contacts.values('id', 'first_name', 'second_name')), safe=False)

def delivery_method_list(request):
    delivery_methods = DeliveryMethod.objects.all()
    return render(request, 'offers/delivery_method_list.html', {'delivery_methods': delivery_methods})

def create_delivery_method(request):
    if request.method == 'POST':
        form = DeliveryMethodForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery method created successfully.')
            return redirect('offers:delivery_method_list')
    else:
        form = DeliveryMethodForm()
    return render(request, 'offers/create_delivery_method.html', {'form': form})

def stage_list(request):
    stages = Stage.objects.all().order_by('order')
    return render(request, 'offers/stage_list.html', {'stages': stages})

def create_stage(request):
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stage created successfully.')
            return redirect('offers:stage_list')
    else:
        form = StageForm()
    return render(request, 'offers/create_stage.html', {'form': form})

def edit_stage(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stage updated successfully.')
            return redirect('offers:stage_list')
    else:
        form = StageForm(instance=stage)
    return render(request, 'offers/edit_stage.html', {'form': form, 'stage': stage})

def delete_stage(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    if request.method == 'POST':
        stage.delete()
        messages.success(request, 'Stage deleted successfully.')
        return redirect('offers:stage_list')
    return render(request, 'offers/delete_stage.html', {'stage': stage})

def offer_stage(request):
    stages = Stage.objects.all().order_by('order')
    if not stages.exists():
        stages = ['Offers']
    
    offers_by_stage = {}
    for stage in stages:
        stage_name = stage.name if isinstance(stage, Stage) else stage
        offers = Offer.objects.filter(stage=stage)
        total_amount = sum(offer.total_amount for offer in offers)
        offers_by_stage[stage_name] = {
            'offers': offers,
            'number_of_offers': offers.count(),
            'total_amount': total_amount,
        }
    
    return render(request, 'offers/offer_stage.html', {'offers_by_stage': offers_by_stage})

def add_offer_product(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.method == 'POST':
        form = OfferProductForm(request.POST)
        if form.is_valid():
            offer_product = form.save(commit=False)
            offer_product.offer = offer
            offer_product.save()
            messages.success(request, 'Offer product added successfully.')
            return redirect('offers:offer_detail', pk=offer.pk)
    else:
        product_id = request.GET.get('product_id')
        form = OfferProductForm(product_id=product_id)
    return render(request, 'offers/add_offer_product.html', {'form': form, 'offer': offer})

def edit_offer_product(request, offer_id, offer_product_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer_product = get_object_or_404(OfferProduct, pk=offer_product_id)
    if request.method == 'POST':
        form = OfferProductForm(request.POST, instance=offer_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer product updated successfully.')
            return redirect('offers:offer_detail', pk=offer.pk)
    else:
        form = OfferProductForm(instance=offer_product)
    return render(request, 'offers/edit_offer_product.html', {'form': form, 'offer': offer, 'offer_product': offer_product})

def delete_offer_product(request, offer_id, offer_product_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer_product = get_object_or_404(OfferProduct, pk=offer_product_id)
    if request.method == 'POST':
        offer_product.delete()
        messages.success(request, 'Offer product deleted successfully.')
        return redirect('offers:offer_detail', pk=offer.pk)
    return render(request, 'offers/delete_offer_product.html', {'offer_product': offer_product, 'offer': offer})

def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer updated successfully.')
            return redirect('offers:offer_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})

def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'Offer deleted successfully.')
        return redirect('offers:list')
    return render(request, 'offers/delete_offer.html', {'offer': offer})

@csrf_exempt
def update_stage_order(request):
    if request.method == 'POST':
        order = request.POST.getlist('order[]')
        for index, stage_id in enumerate(order):
            stage = Stage.objects.get(pk=stage_id)
            stage.order = index
            stage.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)