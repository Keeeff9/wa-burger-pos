from django.urls import include, path
from . import views

urlpatterns = [

    path('invoice/',views.generate_invoice,name='invoice'),
       
]