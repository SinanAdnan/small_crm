from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Company, Contact
from .forms import CompanyForm, ContactForm

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
    return render(request, 'company/company_detail.html', {'company': company, 'contacts': contacts})

# Add Contact View
def add_contact(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)  # Include request.FILES to handle the file upload
        if form.is_valid():
            contact = form.save(commit=False)
            contact.company = Company.objects.get(id=company_id)  # Ensure the contact is linked to the correct company
            contact.save()
            return redirect('company:company_detail', pk=company_id)  # Redirect after saving the form
        else:
            form = ContactForm()

    return render(request, 'company/add_contact.html', {'form': form, 'company': company})

# Edit Contact View
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
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

    return render(request, 'company/delete_company.html', {'company': company})

# Personnel view
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'company/contact_detail.html', {'contact': contact})