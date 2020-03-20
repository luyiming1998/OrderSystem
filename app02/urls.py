"""OrderSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app02 import views
from django.conf import settings
from django.conf.urls.static import static
from app03 import views as v3

urlpatterns = [
    path('goodsmanage/',views.goodsmanage),
    path('display/',views.display),
    path('updateuser/',views.updateuser),
    path('user_order/',views.user_order),
    path('address/',views.address),
    path('add_address/',views.add_address),
    path('del_address/',views.del_address),
    path('edit_address/',views.edit_address),
    path('search_store/',views.search_store),
    path('CommentOrder/',views.CommentOrder),
    path('cart/',views.cart),
    path('order_detail/',views.order_detail),
    path('showimg/',views.showimg),
    path('register/', v3.userregister),
    path('logout/',views.logout),
]