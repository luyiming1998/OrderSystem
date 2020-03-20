from django.contrib import admin
from django.urls import path
from app01 import views
from app03 import views as v3
urlpatterns = [
    path('index/', views.index),
    path('goodsmanage/',views.goodsmanage),
    path('addgood/',views.addgood),
    path('goodtypemanage/', views.goodtypemanage),
    path('addgoodtype/',views.addgoodtype),
    path('delgoodtype/',views.delgoodtype),
    path('updategood/<int:good_id>',views.updategood),
    path('delgood/<int:good_id>', views.delgood),
    path('searchgood/', views.searchgood),
    path('update_good_num/',views.update_good_num),
    path('orderhall/',views.orderhall),
    path('update_order_status/',views.update_order_status),
    path('ordermanage/',views.ordermanage),
    path('orderdetail/<int:order_id>',views.orderdetail),
    path('searchorder/',views.searchorder),
    path('earnmanage/',views.earnmanage),
    path('echart/',views.echart),
    path('updatepwd/',views.updatepwd),
    path('updateinfo/',views.updateinfo),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/',v3.storeregister),
]