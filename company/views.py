from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Company, Contact
from .forms import CompanyForm, ContactForm
from offers.models import Offer
from collections import defaultdict
from django.db.models import Sum
from datetime import date, timedelta
import calendar

# Utility function for redirection
def redirect_to_company_list():
    return HttpResponseRedirect(reverse('company:company_list'))

# Company List View
def company_list(request):
    search_query = request.GET.get('search', '')  # Search query
    country_filter = request.GET.get('country', '')  # Country filter
    companies = Company.objects.all()  # Fetch all companies
    contacts = Contact.objects.all()  # Fetch all contacts

    # Filter companies and contacts based on the search query
    if search_query:
        companies = companies.filter(name__icontains=search_query)
        contacts = contacts.filter(
            first_name__icontains=search_query
        ) | contacts.filter(
            second_name__icontains=search_query
        ) | contacts.filter(
            email__icontains=search_query
        )

    # Filter companies based on the country filter
    if country_filter:
        companies = companies.filter(country=country_filter)

    # Get distinct countries for the filter dropdown
    countries = Company.objects.values_list('country', flat=True).distinct()

    return render(request, 'company/company_list.html', {
        'companies': companies,
        'contacts': contacts,
        'countries': countries,
        'search_query': search_query,
        'country_filter': country_filter
    })

# Company Detail View
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    contacts = company.contacts.all()
    offers = Offer.objects.filter(company=company).order_by('offer_date')

    # Process offers by month for the last 12 months
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    offers = offers.filter(offer_date__gte=one_year_ago)

    monthly_offers = defaultdict(Decimal)
    for offer in offers:
        month = offer.offer_date.strftime('%Y-%m')
        monthly_offers[month] += offer.total_amount

    # Create cumulative totals, monthly totals, and performance changes
    cumulative_totals = []
    monthly_totals = []
    performance_changes = []
    running_total = Decimal('0')
    months = [(today - timedelta(days=30*i)).strftime('%Y-%m') for i in range(11, -1, -1)]
    previous_total = Decimal('0')
    for month in months:
        running_total += monthly_offers[month]
        cumulative_totals.append({
            'month': calendar.month_name[int(month.split('-')[1])],
            'total': float(running_total)
        })
        monthly_totals.append({
            'month': calendar.month_name[int(month.split('-')[1])],
            'total': float(monthly_offers[month])
        })
        performance_change = max(float(monthly_offers[month]) - float(previous_total), 0)
        performance_changes.append(performance_change)
        previous_total = monthly_offers[month]

    total_amount = sum(offer.total_amount for offer in offers)
    context = {
        'company': company,
        'contacts': contacts,
        'offers': offers,
        'total_amount': total_amount,
        'total_offers': offers.count(),
        'cumulative_totals': cumulative_totals,
        'monthly_totals': monthly_totals,
        'performance_changes': performance_changes
    }
    return render(request, 'company/company_detail.html', context)

# Add Contact View
def add_contact(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)  # Include request.FILES to handle file upload
        if form.is_valid():
            contact = form.save(commit=False)
            contact.company = company
            contact.save()
            return redirect('company:company_detail', pk=company_id)  # Redirect after saving the form

    return render(request, 'company/add_contact.html', {'form': form, 'company': company})

# Edit Contact View
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('company:company_detail', pk=contact.company.id)

    form = ContactForm(instance=contact)
    return render(request, 'company/edit_contact.html', {'form': form, 'contact': contact})

# Delete Contact View
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('company:company_detail', pk=contact.company.pk)

    return render(request, 'company/confirm_delete_contact.html', {'contact': contact})

# Add Company View
def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/companies')  # Redirect to the company list after saving
    else:
        form = CompanyForm()  # Instantiate an empty form for the GET request

    # Return the response with the form
    return render(request, 'company/add_company.html', {'form': form})

# Edit Company View
def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect_to_company_list()

    form = CompanyForm(instance=company)
    return render(request, 'company/edit_company.html', {'form': form, 'company': company})

# Delete Company View
def delete_company(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        company.delete()
        return redirect_to_company_list()

    return render(request, 'company/confirm_delete_company.html', {'company': company})

# Contact Detail View
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'company/contact_detail.html', {'contact': contact})