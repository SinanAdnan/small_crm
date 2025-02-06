from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Offer
from .forms import OfferForm

def create_offer(request):
    if request.method == "POST":
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