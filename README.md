# NovaStore — Animated Django Product Sales Site

A Django e-commerce demo with:
- Product catalog with category filtering & search
- Animated hero section, floating cards, scroll-reveal animations (AOS)
- Hover/zoom effects on product cards, discount badges
- Session-based shopping cart (add/remove, live count badge)
- Checkout flow with an animated success confirmation
- Django admin for managing products, categories, and orders

## 1. Setup

```bash
cd shop
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## 2. Configure the database

```bash
python manage.py makemigrations store
python manage.py migrate
```

## 3. Create an admin user

```bash
python manage.py createsuperuser
```

## 4. Load sample products (optional but recommended)

```bash
python manage.py seed_products
```

This creates 4 categories and 8 sample products with stock images, so the
site looks complete immediately.

## 5. Run the server

```bash
python manage.py runserver
```

Visit:
- **Storefront:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

## Project structure

```
shop/
├── manage.py
├── requirements.txt
├── shop/                # project settings, urls, wsgi/asgi
└── store/                # the store app
    ├── models.py         # Category, Product, Order, OrderItem
    ├── views.py          # home, product_detail, cart, checkout
    ├── cart.py           # session-based cart class
    ├── admin.py
    ├── management/commands/seed_products.py
    ├── templates/store/  # base, home, product_detail, cart, checkout, order_success
    └── static/store/     # style.css (animations), script.js
```

## Customizing

- **Add real product photos:** upload via the admin `image` field, or set
  `image_url` to any image link — the template falls back to it automatically.
- **Change colors/animations:** edit the CSS variables and `@keyframes` at
  the top of `store/static/store/css/style.css`.
- **Payments:** checkout currently just records an `Order` in the database
  (no real payment gateway). Wire in Stripe/PayPal in `views.checkout` when
  you're ready to accept real payments.

## Notes

- `DEBUG = True` and a placeholder `SECRET_KEY` are set for local development
  only — change both before deploying anywhere public.
- Animations use [AOS](https://michalsnik.github.io/aos/) (via CDN) for
  scroll-reveal effects, plus custom CSS for hover/float/pulse/success-check
  animations — no extra JS animation library needed.
