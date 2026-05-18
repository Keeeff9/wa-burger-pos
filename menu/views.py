import json
from django.shortcuts import render
from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db import products_collection
from .models import Product


# GET /menu/
def menu_list(request):
    if request.method == "GET":
        products = list(products_collection.find())
        for product in products:
            product["id"] = str(product["_id"])  
            del product["_id"]                   
        return render(request, "menu/menu_list.html", {"products": products})


# GET /menu/<id>/
def product_detail(request, id):
    if request.method == "GET":
        product = products_collection.find_one({"_id": ObjectId(id)})
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
        product["_id"] = str(product["_id"])
        return JsonResponse(product)


# POST /menu/add/
@csrf_exempt
def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body)

        product = Product(
            name=data.get("name"),
            price=data.get("price"),
            category=data.get("category"),
            has_stock=data.get("has_stock"),
            description=data.get("description", ""),
            image_url=data.get("image_url", ""),
        )

        errors = product.is_valid()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = products_collection.insert_one(product.to_dict())
        return JsonResponse({"inserted_id": str(result.inserted_id)}, status=201)


# POST /menu/<id>/update/
@csrf_exempt
def update_stock(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        has_stock = data.get("has_stock")

        if not isinstance(has_stock, bool):
            return JsonResponse({"error": "has_stock must be true or false"}, status=400)

        result = products_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"has_stock": has_stock}}
        )

        if result.matched_count == 0:
            return JsonResponse({"error": "Product not found"}, status=404)

        return JsonResponse({"updated": True})