"""
Seed command: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product


CATEGORIES = [
    ("Abayas & Kaftans",   "abayas-kaftans",   "ladies", "Flowing abayas and kaftans for every occasion"),
    ("Evening Gowns",      "evening-gowns",     "ladies", "Stunning gowns for special events"),
    ("Casual Wear",        "casual-wear",       "ladies", "Chic everyday outfits"),
    ("Traditional Attire", "traditional-attire","ladies", "Beautiful traditional outfits"),
    ("Kids Dresses",       "kids-dresses",      "kids",   "Adorable dresses for little girls"),
    ("Kids Traditional",   "kids-traditional",  "kids",   "Mini traditional outfits"),
    ("Kids Party Wear",    "kids-party",        "kids",   "Special occasion outfits for kids"),
]

PRODUCTS = [
    {
        "name": "Midnight Lace Abaya",
        "slug": "midnight-lace-abaya",
        "category": "abayas-kaftans",
        "description": "A breathtaking black lace abaya with intricate floral embroidery and gold trim detailing. Perfect for formal occasions and evening events. Features a flowing silhouette and premium lace fabric that drapes beautifully.",
        "price": "18500.00", "original_price": "22000.00",
        "stock": 15, "available_sizes": "S,M,L,XL,XXL",
        "is_featured": True, "is_new_arrival": False,
    },
    {
        "name": "Royal Gold Kaftan",
        "slug": "royal-gold-kaftan",
        "category": "abayas-kaftans",
        "description": "Luxurious golden kaftan with hand-stitched embellishments and a majestic drape. A statement piece that exudes royalty. Crafted from premium silk-blend fabric with intricate goldwork along the neckline and cuffs.",
        "price": "24000.00", "original_price": None,
        "stock": 8, "available_sizes": "S,M,L,XL",
        "is_featured": True, "is_new_arrival": True,
    },
    {
        "name": "Emerald Evening Gown",
        "slug": "emerald-evening-gown",
        "category": "evening-gowns",
        "description": "A stunning floor-length emerald green gown with off-shoulder design and subtle gold accents. Features a fitted bodice with boning, an elegant A-line silhouette, and a sweeping train. Perfect for galas and formal dinners.",
        "price": "32000.00", "original_price": "38000.00",
        "stock": 5, "available_sizes": "XS,S,M,L,XL",
        "is_featured": True, "is_new_arrival": False,
    },
    {
        "name": "Blush Satin Ball Gown",
        "slug": "blush-satin-ball-gown",
        "category": "evening-gowns",
        "description": "Romantic blush pink satin ball gown with layered tulle underskirt and delicate lace bodice. The voluminous skirt creates a dreamy silhouette. Perfect for weddings, engagement parties, and grand celebrations.",
        "price": "45000.00", "original_price": None,
        "stock": 3, "available_sizes": "XS,S,M,L",
        "is_featured": False, "is_new_arrival": True,
    },
    {
        "name": "Ankara Power Wrap Dress",
        "slug": "ankara-wrap-dress",
        "category": "casual-wear",
        "description": "Vibrant Ankara print wrap dress with modern cut and figure-flattering silhouette. A perfect blend of African tradition and contemporary fashion. The bold print commands attention while remaining effortlessly elegant.",
        "price": "9500.00", "original_price": "12000.00",
        "stock": 25, "available_sizes": "S,M,L,XL,XXL",
        "is_featured": True, "is_new_arrival": True,
    },
    {
        "name": "Classic Ivory Co-ord Set",
        "slug": "ivory-coord-set",
        "category": "casual-wear",
        "description": "Effortlessly chic ivory linen co-ord set featuring wide-leg palazzo trousers and a structured blazer. Clean lines, premium fabric, and timeless design make this perfect for any occasion from brunch to business.",
        "price": "13500.00", "original_price": None,
        "stock": 18, "available_sizes": "XS,S,M,L,XL",
        "is_featured": False, "is_new_arrival": True,
    },
    {
        "name": "Aso-Oke Ceremonial Set",
        "slug": "aso-oke-ceremonial",
        "category": "traditional-attire",
        "description": "Exquisite Aso-Oke ensemble hand-woven in rich burgundy and gold. This complete set includes the blouse fabric and wrapper, ready for customisation by your tailor. A timeless treasure for owambe and traditional ceremonies.",
        "price": "28000.00", "original_price": "33000.00",
        "stock": 10, "available_sizes": "S,M,L,XL,XXL",
        "is_featured": True, "is_new_arrival": False,
    },
    {
        "name": "George Teal & Silver Set",
        "slug": "george-teal-silver",
        "category": "traditional-attire",
        "description": "Premium Indian George wrapper in stunning teal with silver embossing. Includes matching blouse fabric with intricate bead detailing. A classic choice for traditional weddings and christenings.",
        "price": "21000.00", "original_price": None,
        "stock": 12, "available_sizes": "S,M,L,XL",
        "is_featured": False, "is_new_arrival": True,
    },
    {
        "name": "Pink Princess Tutu",
        "slug": "pink-princess-tutu",
        "category": "kids-dresses",
        "description": "Magical layered tutu dress in soft rose pink with glitter overlay and satin bow. Features comfortable cotton lining and an adjustable waist. Perfect for birthday parties, photoshoots, and special occasions.",
        "price": "6500.00", "original_price": "8000.00",
        "stock": 20, "available_sizes": "2-3Y,4-5Y,6-7Y,8-9Y",
        "is_featured": True, "is_new_arrival": False,
    },
    {
        "name": "Floral Smock Dress",
        "slug": "floral-smock-dress",
        "category": "kids-dresses",
        "description": "Sweet floral smocked dress with puff sleeves in soft pastel colours. The handsmocked bodice adds a touch of artisanal charm. Breathable cotton fabric ensures all-day comfort for active little ones.",
        "price": "5200.00", "original_price": None,
        "stock": 22, "available_sizes": "2-3Y,4-5Y,6-7Y,8-9Y,10-11Y",
        "is_featured": True, "is_new_arrival": True,
    },
    {
        "name": "Mini Royale Aso-Oke",
        "slug": "mini-aso-oke",
        "category": "kids-traditional",
        "description": "Adorable mini Aso-Oke set for little royals attending owambes and ceremonies. Perfectly crafted miniature version of the grown-up classic with playful pops of colour. Makes unforgettable family portraits.",
        "price": "8500.00", "original_price": "10000.00",
        "stock": 15, "available_sizes": "2-3Y,4-5Y,6-7Y,8-9Y",
        "is_featured": True, "is_new_arrival": False,
    },
    {
        "name": "Ankara Ruffles Party Dress",
        "slug": "ankara-party-dress",
        "category": "kids-party",
        "description": "Vibrant Ankara party dress for little fashionistas who love to stand out. Bold ruffled sleeves, a full gathered skirt, and premium Ankara fabric make this perfect for parties and celebrations.",
        "price": "7200.00", "original_price": None,
        "stock": 18, "available_sizes": "4-5Y,6-7Y,8-9Y,10-11Y,12-13Y",
        "is_featured": False, "is_new_arrival": True,
    },
]


class Command(BaseCommand):
    help = 'Seed Febz Couture database with sample products'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n🌱 Seeding Febz Couture database...\n'))

        cat_map = {}
        for name, slug, audience, desc in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'audience': audience, 'description': desc}
            )
            cat_map[slug] = cat
            if created:
                self.stdout.write(f'  ✓ Category: {name}')

        for p in PRODUCTS:
            cat = cat_map.get(p['category'])
            if not cat:
                continue
            prod, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'name': p['name'], 'category': cat,
                    'description': p['description'], 'price': p['price'],
                    'original_price': p.get('original_price'),
                    'stock': p['stock'],
                    'available_sizes': p.get('available_sizes', ''),
                    'is_featured': p.get('is_featured', False),
                    'is_new_arrival': p.get('is_new_arrival', False),
                }
            )
            if created:
                self.stdout.write(f'  ✓ Product: {p["name"]}')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded! 12 products ready.\n'))
        self.stdout.write('👑 Next: python manage.py createsuperuser\n')
