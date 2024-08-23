document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodField = document.querySelector('#id_name');
    const bankTransferFields = [
        'id_bank_account_number',
        'id_account_holder_name',
        'id_iban'
    ];
    const creditCardFields = [
        'id_credit_card_number',
        'id_card_holder_name',
        'id_expiration_date',
        'id_cvv'
    ];
    const westernUnionFields = [
        'id_url'
    ];

    function updateFields() {
        const paymentMethod = paymentMethodField.value;

        // Hide all fields initially
        bankTransferFields.concat(creditCardFields, westernUnionFields).forEach(function(fieldId) {
            const field = document.querySelector(`#${fieldId}`);
            if (field) {
                field.parentElement.parentElement.style.display = 'none';
            }
        });

        // Show the relevant fields based on the selected payment method
        if (paymentMethod === 'Bank Transfer') {
            bankTransferFields.forEach(function(fieldId) {
                const field = document.querySelector(`#${fieldId}`);
                if (field) {
                    field.parentElement.parentElement.style.display = '';
                }
            });
        } else if (paymentMethod === 'Credit Card') {
            creditCardFields.forEach(function(fieldId) {
                const field = document.querySelector(`#${fieldId}`);
                if (field) {
                    field.parentElement.parentElement.style.display = '';
                }
            });
        } else if (paymentMethod === 'Western Union') {
            westernUnionFields.forEach(function(fieldId) {
                const field = document.querySelector(`#${fieldId}`);
                if (field) {
                    field.parentElement.parentElement.style.display = '';
                }
            });
        }
    }

    // Initial update on page load
    updateFields();

    // Update fields when payment method changes
    paymentMethodField.addEventListener('change', updateFields);
});
