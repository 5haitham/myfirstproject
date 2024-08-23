from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)

        # Define specific fields for each payment method
        self.bank_transfer_fields = [
            'bank_account_number',
            'account_holder_name',
            'iban',
        ]
        self.credit_card_fields = [
            'credit_card_number',
            'card_holder_name',
            'expiration_date',
            'cvv',
        ]
        self.western_union_fields = [
            'url',
        ]

        # Add CSS class to the fields to identify them in JavaScript
        for field in self.bank_transfer_fields + self.credit_card_fields + self.western_union_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['class'] = 'payment-method-field'

        # Set initial visibility of the fields based on the initial value of the payment method
        initial_payment_method = self.initial.get('name')
        if initial_payment_method:
            self.update_field_visibility(initial_payment_method)

    def update_field_visibility(self, payment_method):
        # Hide all fields initially
        for field in self.bank_transfer_fields + self.credit_card_fields + self.western_union_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['style'] = 'display:none;'

        # Show the relevant fields based on the selected payment method
        if payment_method == 'Bank Transfer':
            for field in self.bank_transfer_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = ''
            if 'url' in self.fields:
                self.fields['url'].widget.attrs['style'] = 'display:none;'
        
        elif payment_method == 'Credit Card':
            for field in self.credit_card_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = ''
            if 'url' in self.fields:
                self.fields['url'].widget.attrs['style'] = 'display:none;'

        elif payment_method == 'Western Union':
            for field in self.western_union_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = ''
            for field in self.bank_transfer_fields + self.credit_card_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = 'display:none;'
        
        else:
            for field in self.bank_transfer_fields + self.credit_card_fields + self.western_union_fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = 'display:none;'

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('name')
        if payment_method:
            self.update_field_visibility(payment_method)
        return cleaned_data
