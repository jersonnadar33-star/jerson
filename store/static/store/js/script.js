document.addEventListener('DOMContentLoaded', function () {
  // Quantity +/- controls on product detail page
  document.querySelectorAll('.qty-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = btn.parentElement.querySelector('.qty-input');
      let value = parseInt(input.value, 10) || 1;
      if (btn.dataset.action === 'increase') value += 1;
      if (btn.dataset.action === 'decrease') value = Math.max(1, value - 1);
      input.value = value;
    });
  });

  // Little "pop" feedback when Add to Cart is clicked
  document.querySelectorAll('.add-form, .add-form-detail').forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.style.transform = 'scale(0.94)';
        setTimeout(function () { btn.style.transform = ''; }, 150);
      }
    });
  });

  // Auto-dismiss toast messages
  document.querySelectorAll('.toast').forEach(function (toast, i) {
    setTimeout(function () {
      toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-8px)';
      setTimeout(function () { toast.remove(); }, 400);
    }, 3500 + i * 300);
  });
});
