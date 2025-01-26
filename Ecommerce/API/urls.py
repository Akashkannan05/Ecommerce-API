from rest_framework.urls import path
from django.conf.urls import handler404

from . import views

urlpatterns=[
    #User
    path("v1/user/create/",views.RegisterViewClass),
    path("v1/user/login/",views.LoginViewClass),
    path("v1/user/logout/",views.LogoutViewClass),
    #Products
    path("v1/products/",views.ProductListCreateViewClass,name="List the Products or Create the product"),
    path("v1/products/<int:pk>/",views.ProductDetailViewClass,name="Detail of the product"),
    path("v1/products/<int:pk>/update/",views.ProductUpdateViewClass,name="Update the product"),
    path("v1/products/<int:pk>/delete/",views.ProductDeleteViewClass,name="Destroy the product"),
    #Categories
    path("v1/categories/",views.CategoryListCreatViewClass,name="List the categories or Create the category"),
    path("v1/categories/<int:pk>/",views.CategoryDetailViewClass,name="Detail of the category"),
    path("v1/categories/<int:pk>/delete/",views.CategoryDeleteViewClass,name="Delete the category"),
    #Orders
    path("v1/order/",views.ListOrderViewClass,name="List the order"),
    path("v1/order/<int:pk>/detail/",views.OrderDetailViewClass,name="Detail_order"),
    path("v1/order/<int:pk>/update/",views.OrderStatusUpdateViewClass,name="Update the status of the order"),
    #Search
    #If we use <str:key> method we can't get the sapce i think
    path("v1/search/",views.searchViewClass,name="Search"),
    #Cart
    path("v1/cart/",views.CartAddListViewClass,name="Add or list the cart items"),
    path("v1/cart/<int:pk>/",views.CartDetailViewclass,name="Detail of the cart"),
    path('v1/cart/<int:pk>/delete/',views.CartRemoveViewClass,name="Remove the element from the cart")
]

handler404=views.PageNotFoundViewClass