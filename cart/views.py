import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


MOCK_MONGO_SESSION_CACHE = {}

def get_cart_instance(request):
    user_token = request.COOKIES.get('pos_device_token')
    if not user_token:
        user_token = "anonymous_default_session"

    if user_token not in MOCK_MONGO_SESSION_CACHE:
        MOCK_MONGO_SESSION_CACHE[user_token] = {}
    return MOCK_MONGO_SESSION_CACHE[user_token]

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = str(data.get('id'))

        user_cart = get_cart_instance(request)

        if product_id in user_cart:
            user_cart[product_id]['quantity'] += 1
        else:
            user_cart[product_id] = {
                'name': data.get('name'),
                'price': float(data.get('price')),
                'quantity': 1
            }

        total_price = sum(item['price'] * item['quantity'] for item in user_cart.values())
        total_items = sum(item['quantity'] for item in user_cart.values())

        return JsonResponse({'status': 'ok', 'total_items': total_items, 'total_price': total_price})


@csrf_exempt
def remove_from_cart(request):
    if request.method == 'DELETE':
        product_id = str(data.get('id'))



def cart_view(request):
    customer = request.session.get('customer', None)
    user_cart = get_cart_instance(request)
    total_price = sum(item['price'] * item['quantity'] for item in user_cart.values())
    total_items = sum(item['quantity'] for item in user_cart.values())

    context = {
        'cart_items': user_cart,
        'total_price': total_price,
        'total_items': total_items,
        'customer': customer
    }
    return render(request, 'cart.html', context)