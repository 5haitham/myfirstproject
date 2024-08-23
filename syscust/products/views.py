from django.shortcuts import render
from .models import product
def productt(request):
    return render(request,'products/product.html')
pro = product.objects.all()
def products(request):
    return render(request,'products/products.html',{'pro':product.objects.all()})
