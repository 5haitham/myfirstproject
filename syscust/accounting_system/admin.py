from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Invoice, InvoiceItem, Subscriber, Subscribe, Expense, PaymentMethod
from .forms import PaymentMethodForm  # استيراد النموذج المخصص

# فلتر مخصص للرصيد
class BalanceFilter(admin.SimpleListFilter):
    title = 'الرصيد'
    parameter_name = 'balance'

    def lookups(self, request, model_admin):
        return [
            ('zero', 'صفر'),
            ('positive', 'إيجابي'),
            ('negative', 'سلبي'),
            ('low', 'أقل من 100'),
            ('medium', 'بين 100 و 500'),
            ('high', 'أكثر من 500'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'zero':
            return queryset.filter(balance=0)
        elif value == 'positive':
            return queryset.filter(balance__gt=0)
        elif value == 'negative':
            return queryset.filter(balance__lt=0)
        elif value == 'low':
            return queryset.filter(balance__lt=100)
        elif value == 'medium':
            return queryset.filter(balance__gte=100, balance__lte=500)
        elif value == 'high':
            return queryset.filter(balance__gt=500)
        return queryset

class PaymentMethodAdmin(admin.ModelAdmin):
    form = PaymentMethodForm
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

    class Media:
        js = ('payment_method.js',)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['product', 'quantity', 'price', 'total']
    readonly_fields = ['total']
    verbose_name = 'عنصر الفاتورة'
    verbose_name_plural = 'عناصر الفاتورة'

def print_invoice(modeladmin, request, queryset):
    if queryset.count() == 1:
        invoice = queryset.first()
        html = render_to_string('accounting_system/invoice_print.html', {'invoice': invoice})
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = f'inline; filename=invoice_{invoice.id}.html'
        return response
    else:
        modeladmin.message_user(request, "يرجى تحديد فاتورة واحدة فقط للطباعة", level='error')

print_invoice.short_description = 'طباعة الفاتورة'

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date', 'due_date', 'total', 'payment', 'balance', 'status', 'payment_method']
    list_filter = ['status', 'payment_method', 'date', BalanceFilter]  # أضف الفلتر المخصص هنا
    fieldsets = (
        (None, {
            'fields': ('client', 'due_date', 'total', 'payment', 'balance', 'payment_method',)
        }),
        ('معلومات إضافية', {
            'fields': ('date',),
            'classes': ('collapse',),
        }),
    )
    inlines = [InvoiceItemInline]
    actions = [print_invoice]
    readonly_fields = ['date']
    verbose_name = 'فاتورة'
    verbose_name_plural = 'الفواتير'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            cl = response.context_data['cl']
            queryset = cl.queryset.aggregate(total_amount=Sum('total'))
            response.context_data['total_amount'] = queryset['total_amount']
        return response

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subscriber_balance', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']
    verbose_name = 'مشترك'
    verbose_name_plural = 'المشتركون'

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    verbose_name = 'اشتراك'
    verbose_name_plural = 'الاشتراكات'

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'date', 'description']
    search_fields = ['category', 'description']
    list_filter = ['date', 'category']
    verbose_name = 'مصروف'
    verbose_name_plural = 'المصروفات'

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
