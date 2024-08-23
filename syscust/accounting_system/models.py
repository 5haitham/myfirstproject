from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum
from django_jsonfield_backport.models import JSONField
from django.core.exceptions import ValidationError

class Subscriber(models.Model):
    name = models.CharField(max_length=255, verbose_name='الاسم')
    address = models.TextField(blank=True, null=True, verbose_name='العنوان')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='الهاتف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    subscriber_balance = models.CharField(max_length=50, blank=True, null=True, verbose_name='رصيد المشترك')

    def __str__(self):
        return self.name

    def update_batch(self):
        total_balance = self.invoices.aggregate(total_balance=Sum('balance'))['total_balance'] or 0.00
        self.subscriber_balance = f"{total_balance:.2f}"
        self.save(update_fields=['subscriber_balance'])

    class Meta:
        verbose_name = 'مشترك'
        verbose_name_plural = 'المشتركون'

@receiver(pre_delete, sender=Subscriber)
def prevent_subscriber_delete_if_invoices_exist(sender, instance, **kwargs):
    if instance.invoices.exists():
        raise ValidationError("لا يمكن حذف المشترك لوجود فواتير مرتبطة به.")

class Subscribe(models.Model):
    name = models.CharField(max_length=255, verbose_name='الاسم')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'اشتراك'
        verbose_name_plural = 'الاشتراكات'

class PaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'كاش'),
        ('Credit Card', 'كريدت كارد'),
        ('Bank Transfer', 'حوالة بنكية'),
        ('Western Union', 'ويسترن يونيون')
    ]

    name = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='طريقة الدفع')
    url = models.URLField(blank=True, null=True, verbose_name='الرابط')  # حقل الرابط الجديد

    # Fields for Bank Transfer
    bank_account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='رقم الحساب')
    account_holder_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='اسم المستفيد')
    iban = models.CharField(max_length=34, blank=True, null=True, verbose_name='الايبان')

    # Fields for Credit Card
    credit_card_number = models.CharField(max_length=16, blank=True, null=True, verbose_name='رقم بطاقة الائتمان')
    card_holder_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='اسم حامل البطاقة')
    cvv = models.CharField(max_length=4, blank=True, null=True, verbose_name='رمز CVV')

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'طريقة الدفع'
        verbose_name_plural = 'طرق الدفع'

@receiver(pre_delete, sender=PaymentMethod)
def prevent_payment_method_delete_if_invoices_exist(sender, instance, **kwargs):
    if instance.invoice_set.exists():
        raise ValidationError("لا يمكن حذف طريقة الدفع لوجود فواتير مرتبطة بها.")

class Invoice(models.Model):
    client = models.ForeignKey(Subscriber, related_name='invoices', on_delete=models.CASCADE, verbose_name='العميل')
    date = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ')
    due_date = models.DateField(verbose_name='تاريخ الاستحقاق')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='الإجمالي')
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='الدفعة')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='الرصيد')
    status = models.CharField(max_length=20, choices=[('Paid', 'مسددة'), ('Partially Paid', 'مسددة جزئيا'), ('Unpaid', 'غير مسددة')], default='Unpaid', verbose_name='الحالة')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='طريقة الدفع')

    def __str__(self):
        return f"فاتورة {self.id} للعميل {self.client.name}"

    def save(self, *args, **kwargs):
        self.update_balance_and_status()
        super().save(*args, **kwargs)

    def update_total(self):
        total = sum(item.total for item in self.items.all())
        self.total = total
        self.update_balance_and_status()
        self.save(update_fields=['total', 'balance', 'status'])

    def update_balance_and_status(self):
        self.balance = self.total - self.payment if self.payment else self.total
        if self.payment >= self.total:
            self.status = 'Paid'
        elif 0 < self.payment < self.total:
            self.status = 'Partially Paid'
        else:
            self.status = 'Unpaid'

    class Meta:
        verbose_name = 'فاتورة'
        verbose_name_plural = 'الفواتير'

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE, verbose_name='الفاتورة')
    product = models.ForeignKey(Subscribe, on_delete=models.CASCADE, verbose_name='المنتج')
    quantity = models.IntegerField(default=1, verbose_name='الكمية')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='السعر')
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00, verbose_name='الإجمالي')

    def get_total(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        self.total = self.get_total()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'عنصر الفاتورة'
        verbose_name_plural = 'عناصر الفاتورة'

@receiver(pre_save, sender=InvoiceItem)
def set_price_from_product(sender, instance, **kwargs):
    if instance.product and (instance.price is None or instance.price == 0):
        instance.price = instance.product.price

@receiver(post_save, sender=InvoiceItem)
def update_invoice_total_post_save(sender, instance, **kwargs):
    if instance.invoice:
        instance.invoice.update_total()

@receiver(post_delete, sender=InvoiceItem)
def update_invoice_total_post_delete(sender, instance, **kwargs):
    if instance.invoice:
        instance.invoice.update_total()

@receiver(post_save, sender=Invoice)
def update_subscriber_batch_post_save(sender, instance, **kwargs):
    if instance.client:
        instance.client.update_batch()

@receiver(post_delete, sender=Invoice)
def update_subscriber_batch_post_delete(sender, instance, **kwargs):
    if instance.client:
        instance.client.update_batch()

class Expense(models.Model):
    category = models.CharField(max_length=100, verbose_name='الفئة')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    date = models.DateField(verbose_name='التاريخ')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    attachment = models.FileField(upload_to='expenses/', blank=True, null=True, verbose_name='المرفق')

    def __str__(self):
        return f"{self.category} - {self.amount}"

    class Meta:
        verbose_name = 'مصروف'
        verbose_name_plural = 'المصروفات'
