# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
        })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
            return redirect('products:product_detail', pk=product.pk)  
        else:
            print(form.errors)  # Debugging: print errors to console
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_delete.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

# View to add a new category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')  # Redirect to category list after adding
    else:
        form = CategoryForm()
    
    return render(request, 'products/add_category.html', {'form': form})

# Edit an existing category
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

# Delete a category
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})