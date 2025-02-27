from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from offers.models import OfferProduct
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta


def product_list(request):
    products = Product.objects.all()  # Get all products
    
    # Get filter parameters from request
    search_query = request.GET.get('search', '')  # Get search query from request
    size_filter = request.GET.get('size', '')  # Get size filter
    material_filter = request.GET.get('material', '')  # Get material filter
    model_filter = request.GET.get('model', '')  # Get model filter

    # Apply search filter if a search term is provided
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    # Apply additional filters
    if size_filter:
        products = products.filter(size__iexact=size_filter)
    if material_filter:
        products = products.filter(material__iexact=material_filter)
    if model_filter:
        products = products.filter(model__iexact=model_filter)

    # Pagination (10 products per page)
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique values for dropdown filters
    sizes = Product.objects.values_list('size', flat=True).distinct()
    materials = Product.objects.values_list('material', flat=True).distinct()
    models = Product.objects.values_list('model', flat=True).distinct()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'size_filter': size_filter,
        'material_filter': material_filter,
        'model_filter': model_filter,
        'sizes': sizes,
        'materials': materials,
        'models': models
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    now = datetime.now().strftime('%Y-%m-%d')

    context = {
        'product': product,
        'now': now
    }

    return render(request, 'products/product_detail.html', context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Save but don't commit to the database yet
            product.save()  # Now save to the database
            messages.success(request, 'Product created successfully!')
            return redirect('products:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:product_list')
    
    return render(request, 'products/product_delete.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'products/add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Edit Category'})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('products:category_list')
    
    return render(request, 'products/category_confirm_delete.html', {'category': category})

def product_detail_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'product_code': product.product_code,
        'name': product.name,
        'size': product.size,
        'material': product.material,
        'unit_cost': product.unit_cost,
        'margin': product.margin,
        'price': product.price,
        'description': product.description,
    }
    return JsonResponse(data)

def product_offer_data(request, product_id):
    offers = OfferProduct.objects.filter(product_id=product_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
    else:
        start_date = datetime.now() - timedelta(days=365)
    
    if end_date:
        end_date = parse_date(end_date)
    else:
        end_date = datetime.now()

    offers = offers.filter(offer__offer_date__range=(start_date, end_date))

    country_data = {}
    company_data = {}

    for offer in offers:
        country = offer.offer.project_country.name
        company = offer.offer.company.name
        quantity = offer.quantity

        if country not in country_data:
            country_data[country] = 0
        country_data[country] += quantity

        if company not in company_data:
            company_data[company] = 0
        company_data[company] += quantity

    return JsonResponse({
        'countries': country_data,
        'companies': company_data,
    })