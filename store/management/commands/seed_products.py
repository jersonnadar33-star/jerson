import urllib.request
from urllib.error import URLError

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import Category, Product


CATEGORIES = ['Audio', 'Wearables', 'Computing', 'Home']

PRODUCTS = [
    {
        'name': 'Aurora Wireless Headphones',
        'category': 'Audio',
        'price': 129.99,
        'discount': 19,
        'description': 'Immersive spatial sound with 40-hour battery life and adaptive noise cancellation.',
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
        'stock': 25,
        'is_featured': True,
    },
    {
        'name': 'Pulse Smart Watch',
        'category': 'Wearables',
        'price': 199.00,
        'discount': 0,
        'description': 'Track your fitness, sleep, and heart rate with a vivid always-on display.',
        'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
        'stock': 15,
        'is_featured': True,
    },
    {
        'name': 'Nimbus Ultralight Laptop',
        'category': 'Computing',
        'price': 1299.00,
        'discount': 13,
        'description': 'A featherweight powerhouse with a stunning display and all-day battery.',
        'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80',
        'stock': 8,
        'is_featured': True,
    },
    {
        'name': 'Orbit Smart Speaker',
        'category': 'Home',
        'price': 79.99,
        'discount': 0,
        'description': 'Room-filling sound with a built-in voice assistant and warm ambient lighting.',
        'image_url': 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&q=80',
        'stock': 40,
        'is_featured': True,
    },
    {
        'name': 'Zenith Mechanical Keyboard',
        'category': 'Computing',
        'price': 89.00,
        'discount': 18,
        'description': 'Tactile, satisfying keystrokes with per-key RGB backlighting.',
        'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
        'stock': 30,
        'is_featured': False,
    },
    {
        'name': 'Halo Noise-Cancelling Earbuds',
        'category': 'Audio',
        'price': 149.00,
        'discount': 0,
        'description': 'Compact earbuds with a charging case and crystal-clear calls.',
        'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80',
        'stock': 20,
        'is_featured': False,
    },
    {
        'name': 'Flux Fitness Band',
        'category': 'Wearables',
        'price': 49.99,
        'discount': 28,
        'description': 'Lightweight activity tracker with 10-day battery and water resistance.',
        'image_url': 'https://images.unsplash.com/photo-1575311373937-4a8b9b0e5b7f?w=800&q=80',
        'stock': 50,
        'is_featured': False,
    },
    {
        'name': 'Drift Smart Thermostat',
        'category': 'Home',
        'price': 119.00,
        'discount': 0,
        'description': 'Learns your schedule and saves energy automatically, controlled from your phone.',
        'image_url': 'https://images.unsplash.com/photo-1567925086983-1a97c02b98d8?w=800&q=80',
        'stock': 12,
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample product data'

    def handle(self, *args, **options):
        cat_map = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, slug=name.lower())
            cat_map[name] = cat

        created_count = 0
        for data in PRODUCTS:
            slug = data['name'].lower().replace(' ', '-')
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'category': cat_map[data['category']],
                    'price': data['price'],
                    'discount': data['discount'],
                    'description': data['description'],
                    'stock': data['stock'],
                    'is_featured': data['is_featured'],
                }
            )
            if created:
                created_count += 1
                self._attach_image(product, data['image_url'])

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created_count} new products across {len(CATEGORIES)} categories.'
        ))

    def _attach_image(self, product, url):
        """Download a sample image and attach it to the product's image field."""
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=10) as response:
                content = response.read()
            filename = f'{product.slug}.jpg'
            product.image.save(filename, ContentFile(content), save=True)
        except (URLError, OSError) as exc:
            self.stdout.write(self.style.WARNING(
                f'Could not download image for "{product.name}" ({exc}). '
                'Add one manually from the admin panel.'
            ))
