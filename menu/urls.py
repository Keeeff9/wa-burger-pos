# menu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_list, name="menu_list"),
    path("add/", views.add_product, name="add_product"),       
    path("<str:id>/", views.product_detail, name="product_detail"), 
    path("<str:id>/update/", views.update_stock, name="update_stock"),
]