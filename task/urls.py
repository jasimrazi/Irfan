from . import views
from django.urls import path

urlpatterns = [
    path("add", views.AddProductView.as_view()),
    path("getproducts", views.GetProductsView.as_view()),
    path("ayisha", views.AyishaView.as_view()),
    path("sagar", views.SagarView.as_view()),
    path("ramees", views.RameesView.as_view()),
    path("shibin", views.ShibinView.as_view()),
    path("sreeyuktha", views.SreeyukthaView.as_view()),
]
