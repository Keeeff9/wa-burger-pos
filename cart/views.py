import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

MOCK_MONGO_SESSION_CACHE = {}

def get_cart_instance(request):
    user_token = request.COOKIES.get('pos_device_token', 'anonymous_default_session')
    return MOCK_MONGO_SESSION_CACHE.setdefault(user_token, {})

def calculate_totals(user_cart):
    total_price = sum(item['price'] * item['quantity']
    for item in user_cart.values())
    total_items = sum(item['quantity']
    for item in user_cart.values())
    return total_items, total_price

@csrf_exempt
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        product_id = str(data.get('id', ''))
        action = data.get('action')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    if not product_id:
        return JsonResponse({'error': 'Missing product id'}, status=400)

    user_cart = get_cart_instance(request)

    if action == 'add':
        name = data.get('name')
        price = data.get('price')

        if not name or price is None:
            return JsonResponse({'error': 'Missing product fields: name, price'}, status=400)

        if product_id in user_cart:
            user_cart[product_id]['quantity'] += 1
        else:
            user_cart[product_id] = {
                'name': name,
                'price': float(price),
                'quantity': 1,
            }
    elif action in ('increment', 'decrement'):
        if product_id not in user_cart:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)

        if action == 'increment':
            user_cart[product_id]['quantity'] += 1
        else:
            user_cart[product_id]['quantity'] -= 1
            if user_cart[product_id]['quantity'] <= 0:
                user_cart.pop(product_id)

    else:
        return JsonResponse({'error': 'Invalid action. Use: add, increment, decrement'}, status=400)
    request.session["cart"] = user_cart
    request.session.modified = True
    total_items, total_price = calculate_totals(user_cart)
    current_item = user_cart.get(product_id)
    item_quantity = current_item['quantity'] if current_item else 0
    item_total = (current_item['price'] * item_quantity) if current_item else 0

    return JsonResponse({
        'status': 'ok',
        'item_removed': product_id not in user_cart,
        'item_quantity': item_quantity,
        'item_total': item_total,
        'total_items': total_items,
        'total_price': total_price,
    })


@csrf_exempt
def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        product_id = str(data.get('id', ''))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    user_cart = get_cart_instance(request)
    user_cart.pop(product_id, None)
    request.session["cart"] = user_cart
    request.session.modified = True
    
    total_items, total_price = calculate_totals(user_cart)
    return JsonResponse({
        'status': 'ok',
        'total_items': total_items,
        'total_price': total_price,
    })


def cart_view(request):
    user_cart = get_cart_instance(request)
    total_items, total_price = calculate_totals(user_cart)

    context = {
        'cart_items': user_cart,
        'total_price': total_price,
        'total_items': total_items,
        'customer': request.session.get('customer', None)
    }
    return render(request, 'cart.html', context)