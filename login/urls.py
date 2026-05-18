# menu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_main, name="show_login"),
    path("users/", views.show_users, name="get_all_users"),
    path("add/", views.add_user, name="add_user"),
    path("add_form/", views.add_user_from_form, name="add_user_from_form"),
    path("<str:id>/", views.get_user, name="get_user"),
    path("find/<str:document_id>/", views.search_person, name="get_user_by_document"),
    path("update/<str:id>/", views.update_user, name="update_user"),
]