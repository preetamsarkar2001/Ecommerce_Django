# helpers.py (or similar)
from ecomm.models import *
def calculate_cart_total(request):
    cart_items = get_cart_items(request)
    total = sum(item['product'].price * item['quantity'] for item in cart_items)
    return total

def get_cart_items(request):
    # Replace with your actual logic for fetching cart items
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=[item['product_id'] for item in cart])
    cart_items = []
    for item in cart:
        product = products.get(id=item['product_id'])
        cart_items.append({'product': product, 'quantity': item['quantity']})
    return cart_items

def clear_cart(request):
    request.session['cart'] = []
