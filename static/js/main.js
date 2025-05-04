// Main JavaScript file for Overseas Trading

document.addEventListener('DOMContentLoaded', function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]'),
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Form validation
  var forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      'submit',
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      },
      false,
    );
  });

  // Currency formatter for input fields
  var currencyInputs = document.querySelectorAll('.currency-input');
  currencyInputs.forEach(function (input) {
    input.addEventListener('blur', function () {
      var value = parseFloat(this.value.replace(/[^0-9.-]+/g, ''));
      if (!isNaN(value)) {
        this.value = value.toFixed(2);
      }
    });
  });

  // Quantity input validation
  var quantityInputs = document.querySelectorAll('.quantity-input');
  quantityInputs.forEach(function (input) {
    input.addEventListener('input', function () {
      var value = parseInt(this.value);
      if (isNaN(value) || value < 1) {
        this.value = 1;
      }
    });
  });

  // Order item calculation
  var orderItemForms = document.querySelectorAll('.order-item-form');
  orderItemForms.forEach(function (form) {
    var quantityInput = form.querySelector('.quantity-input');
    var rateInput = form.querySelector('.rate-input');
    var amountInput = form.querySelector('.amount-input');

    function calculateAmount() {
      var quantity = parseFloat(quantityInput.value) || 0;
      var rate = parseFloat(rateInput.value) || 0;
      var amount = quantity * rate;
      amountInput.value = amount.toFixed(2);
    }

    if (quantityInput && rateInput && amountInput) {
      quantityInput.addEventListener('input', calculateAmount);
      rateInput.addEventListener('input', calculateAmount);
    }
  });
});
