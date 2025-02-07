from django.shortcuts import render, redirect, get_object_or_404
from .models import Offer, OfferCounter
from .forms import OfferForm, InitializeCounterForm

def initialize_counter(request):
    if request.method == 'POST':
        form = InitializeCounterForm(request.POST)
        if form.is_valid():
            initial_number = form.cleaned_data['initial_number']
            counter, created = OfferCounter.objects.get_or_create(pk=1)
            counter.base_number = initial_number
            counter.current_number = initial_number
            counter.save()
            return redirect('offers:list')
    else:
        form = InitializeCounterForm()
    return render(request, 'offers/initialize_counter.html', {'form': form})

def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offers:list')
    else:
        form = OfferForm()
    return render(request, 'offers/create_offer.html', {'form': form})

def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'offers/offer_list.html', {'offers': offers})

def offer_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'offers/offer_detail.html', {'offer': offer})