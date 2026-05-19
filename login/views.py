from bson import ObjectId
from bson.errors import InvalidId
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json

from .db import persons_collection
from .models import Person


def show_main(request):
    return render(request, "login/index.html")

# GET /login

def show_users(request):
    if request.method == "GET":
        persons = list(persons_collection.find())
        for person in persons:
            person["_id"] = str(person["_id"])  # ObjectId a string
        return JsonResponse(persons, safe=False)
    return None


# GET /login/<id>/
def get_user(request, id):
    if request.method == "GET":
        person = persons_collection.find_one({"_id": ObjectId(id)})
        if not person:
            return JsonResponse({"error": "Person not found"}, status=404)
        person["_id"] = str(person["_id"])
        return JsonResponse(person)
    return None

# GET /login/find/<document-id>
def search_person(request, document_id):
    if request.method == "GET":
        person = persons_collection.find_one({"document": document_id})

        if person:
            # request.session['customer'] = {
            #     'document': document_id,
            #     'name': person.get('name', ""),
            # }
            return JsonResponse({
                "found": True,
                "name": person.get("name", ""),
                "email": person.get("email", ""),
                "phone": person.get("phone", "")
            })
        else:
            return JsonResponse({"found": False}, status=404)
    return None


# POST /login/add/
@csrf_exempt
def add_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        person = Person(
            name=data.get("name"),
            document=data.get("document"),
            email=data.get("email"),
            phone=data.get("phone"),
            invoices=data.get("invoices"),
        )

        errors = person.is_valid()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = persons_collection.insert_one(person.to_dict())
        return JsonResponse({"inserted_id": str(result.inserted_id)}, status=201)
    return None

def add_user_from_form(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    document = request.POST.get("documentId")

    existing_person = persons_collection.find_one({
        "document": document
    })

    # request.session['customer'] = {
    #     'document': document,
    #     'name': request.POST.get("name")
    # }

    if existing_person:
        return redirect("/menu")

    person = Person(
        name=request.POST.get("name"),
        document=document,
        email=request.POST.get("email"),
        phone=request.POST.get("phone"),
        invoices=[]
    )

    errors = person.is_valid()

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    result = persons_collection.insert_one(person.to_dict())

    return redirect("/menu")


# POST /login/<id>/update/
def update_user(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT method allowed"}, status=405)

    try:
        object_id = ObjectId(id)
    except InvalidId:
        return JsonResponse({"error": "Invalid ID"}, status=400)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    updated_data = {
        "name": body.get("name"),
        "document": body.get("document"),
        "email": body.get("email"),
        "phone": body.get("phone"),
    }

    result = persons_collection.update_one(
        {"_id": object_id},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        return JsonResponse({"error": "Person not found"}, status=404)

    person = persons_collection.find_one({"_id": object_id})
    person["_id"] = str(person["_id"])

    return JsonResponse({
        "message": "Person updated successfully",
        "person": person
    })