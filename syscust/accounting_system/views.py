from django.shortcuts import render
from .models import Subscriber
from .models import Subscribe
from .models import Invoice
from .models import InvoiceItem
from .models import Expense

# Create your views here.




def Subscriber_list(request):
    clients = Subscriber.objects.all()
    return render(request, 'subscribelist.html', {'clients': clients})

def Subscriber_detail(request, pk):
    client = Subscriber.objects.get(pk=pk)
    return render(request, 'subscriberdetails.html', {'client': client})

def invoice(request):
    x = Invoice.objects.all()
    return render(request, 'accounting_system/invoice_print.html',{'invoice':x})




