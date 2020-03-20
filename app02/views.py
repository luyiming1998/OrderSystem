from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.shortcuts import render, redirect, HttpResponse
from django.forms import Form
from django.forms import fields
from app01.models import *
from app02.forms import AddressAdd
import json
#用户美食
def goodsmanage(request):
    if request.method == 'GET':
        stores_list1 = Stores.objects.all().order_by('store_id')
        current_page = request.GET.get('page')
        paginator = Paginator(stores_list1, 8)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger as e:
            posts = paginator.page(1)
            print(e)
        except EmptyPage as e:
            posts = paginator.page(1)
            print(e)
        return render(request, 'User/GoodsManage.html',{'posts':posts})

from app02.forms import UserOrder
#商家所有商品
def display(request):
        if request.method=='GET':
            id = request.GET.get('store_id')
            good_list = Goods.objects.filter(good_store_id=id).all()
            comment_list = Comment.objects.all()
            store_list = Stores.objects.filter(store_id=id)
            return render(request,'User/detailed.html',{'good_list':good_list,'comment_list':comment_list,'store_list':store_list})
        else:
            ret = {'status': True, 'message': None}
            try:
                user_info=request.session.get("user_info")
                user_id=user_info["user_id"]
                arrs=request.POST.getlist("arryObj")
                store_id=request.POST.get("store_id")
                total_price=request.POST.get("total_price")
                list1=[]
                for good in arrs:
                    good=good.split(",")
                    print(good)
                    list1.append({"id":good[0],"num":good[1],"price":good[2]})
                order=Orders.objects.create(order_store_id=store_id,order_user_id=user_id,total_price=total_price,order_status=1,order_address_id=1)
                for i in list1:
                    Order_details.objects.create(order_id=order.order_id,good_id=i["id"],number=i["num"],discount_price=i["price"])
            except Exception as e:
                ret['status'] = False
                ret['message'] = str(e)
            return HttpResponse(json.dumps(ret))


from app02.forms import UpdateForm


# 修改用户信息
def updateuser(request):
    if request.method == 'GET':
        user_list = Users.objects.filter(user_id=1).values('user_id', 'account', 'pwd', 'user_name', 'user_tel',
                                                                  'user_avatar').first()
        return render(request, 'User/updateuser.html', {'user_list': user_list})
    else:
        obj = UpdateForm(data=request.POST,files=request.FILES)
        if obj.is_valid():
            print(obj.cleaned_data)
            user_id = obj.cleaned_data['user_id']
            accont = obj.cleaned_data['account']
            pwd = obj.cleaned_data['pwd']
            user_name = obj.cleaned_data['user_name']
            user_tel = obj.cleaned_data['user_tel']
            user_avatar = request.FILES.get("user_avatar")
            print(user_avatar)
            if user_avatar:
                user=Users.objects.filter(user_id=user_id).first()
                user.user_avatar=user_avatar
                user.save()
            user_list = Users.objects.filter(user_id=user_id).update(account=accont, pwd=pwd, user_name=user_name,
                                                    user_tel=user_tel)
            user=Users.objects.filter(user_id=user_id).values("user_id","account","pwd","user_avatar","user_name").first()
            if user:
                request.session["user_info"]=user
            return render(request,'User/updateuser.html')
        else:
            print(obj.errors)
            return render(request, 'User/updateuser.html')

def user_order(request):
    if request.method == 'GET':
        order_list = Orders.objects.all().values('order_id', 'create_date', 'order_store__real_name', 'finish_time',
                                                 'total_price')
        return render(request, 'User/order.html', {'order_list': order_list})

# 用户地址管理
def address(request):
    if request.method == 'GET':
        address_list = Address.objects.all().order_by('address_id')
        current_page = request.GET.get('page')
        paginator = Paginator(address_list, 9)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger as e:
            posts = paginator.page(1)
            print(e)
        except EmptyPage as e:
            posts = paginator.page(1)
            print(e)
        return render(request, 'User/address.html', {'posts': posts})
    else:
        pass
        # address_id = request.GET.get('address_id')
        # print(address_id)
        # models.Address.objects.filter(address_id=address_id).update(address_status=0)
        # return redirect('/user/address/')

# 添加地址
def add_address(request):
    ret = {'status': True, 'message': None}
    try:
        obj = AddressAdd(request.GET)
        if obj.is_valid():
            print(obj.cleaned_data)
            user_name = request.GET.get('user_name')
            address_tel = request.GET.get('address_tel')
            sex = request.GET.get('sex')
            location = request.GET.get('location')
            address_list = Address.objects.create(location=location, address_name=user_name, address_tel=address_tel,
                                                  sex=sex, address_user_id=1, address_status=1)
            address_list.save()
            return redirect('/user/address/')
        else:
            print(obj.errors)
            return render(request, 'User/address.html')
    except  Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

# 删除
def del_address(request):
    address_id = request.GET.get('address_id')
    print(address_id)
    Address.objects.filter(address_id=address_id).delete()
    return redirect('/user/address/')


from app02.forms import EditAddress


def edit_address(request):
    if request.method == 'GET':
        address_id = request.GET.get('address_id')
        address_list = Address.objects.filter(address_id=address_id)
        return render(request, 'User/edit_address.html', {'address_list': address_list})
    else:
        obj = EditAddress(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            id = obj.cleaned_data['address_id']
            name = obj.cleaned_data['user_name']
            tel = obj.cleaned_data['address_tel']
            sex = obj.cleaned_data['sex']
            location = obj.cleaned_data['location']
            address = Address.objects.filter(address_id=id).update(location=location, address_name=name,
                                                                   address_tel=tel, sex=sex)
            return redirect('/user/address/')
        else:
            print(obj.errors)
            return render(request, 'User/address.html')


# 搜索商家
def search_store(request):
    store_name = request.GET.get('store_name')
    print(store_name)
    stores_list = Stores.objects.filter(store_name__contains=store_name).values_list("store_id", "real_name",
                                                                                     "store_name",
                                                                                     "store_tel", "remark",
                                                                                     "address",
                                                                                     "identity_card_back",
                                                                                     "identity_card_front",
                                                                                     )
    print(stores_list)
    current_page = request.GET.get('page')
    paginator = Paginator(stores_list, 8)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e:
        posts = paginator.page(1)
        print(e)
    except EmptyPage as e:
        posts = paginator.page(1)
        print(e)
    return render(request, 'User/GoodsManage.html', {'posts': posts, 'store_name': store_name})


# 评论
def CommentOrder(request):
    ret = {'status': True, 'message': None}
    try:
        content = request.POST.get('content')
        print(content)
        Comment.objects.create(comment_content=content, level=1, create_date='2019-12-09 09:06:15', comment_status=1)
    except  Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
        print(str(e))
    return HttpResponse(json.dumps(ret))


# 购物车no
def cart(request):
    ret = {'status': True, 'message': None}
    try:
        good_id = request.GET.get('good_id')
        count = request.GET.get('count')
        list1 = []
        order_list = Orders.objects.all()
        for row in order_list:
            list1.append(row.order_id)
        list2 = []
        goodlist = Goods.objects.filter(good_id=good_id)
        for row in goodlist:
            list2.append(row.price)
        good_details = Order_details.objects.create(number=count, discount_price=list2[0], good_id=good_id,
                                                    order_id=list1[0])
        for row in good_details:
            print(row.number, row.discount_price)
        good_details.save()
        return render(request, 'User/detailed.html',
                      {'goodlist': goodlist, "count": count, 'good_details': good_details})
    except  Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


# 订单详情信息
def order_detail(request):
    order_id = request.GET.get('order_id')
    print(order_id)
    detail = Order_details.objects.filter(order_id=order_id).values('good__good_name', 'number', 'discount_price',
                                                                    'order__total_price')

    return render(request, 'User/order_detail.html', {"detail_list": detail})


def showimg(request):
    imgs = Users.objects.filter(user_id=1)
    context={
        'img':imgs
    }

    return render(request,'User/userbase.html',context)


def logout(request):
    if request.session.get("user_info"):
        del request.session['user_info']
    return redirect("/login/")