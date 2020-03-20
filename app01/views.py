import json

from django.shortcuts import render, redirect, HttpResponse
import datetime
from utils.pager import PageInfo
from .form import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.db.models import F, Q, Count, Sum
from pyecharts.charts import Bar
from pyecharts import options as opts


# Create your views here.
def index(request):
    return render(request, "Store/storebase.html")


def login(request):
    # if request.method=="GET":
    #     return render(request,"Store/StoreLogin.html")
    # else:
    account = "admin"
    pwd = "123456789"
    store_info = Stores.objects.filter(account=account, pwd=pwd, store_status__gte=1).values("store_id", "store_name",
                                                                                             "pwd", "store_avatar")
    print(store_info)
    request.session["store_info"] = store_info[0]
    return redirect("/store/orderhall/")


def logout(request):
    if request.session.get("store_info"):
        del request.session['store_info']
    return redirect("/login/")


def goodsmanage(request):
    """
    商品管理
    :param request:
    :return:
    """
    if request.method == "GET":
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        goods_list = Goods.objects.filter(good_store_id=store_id, good_status__gte=1).all().values_list("good_id",
                                                                                                        "good_pic",
                                                                                                        "good_name",
                                                                                                        "price",
                                                                                                        "discount",
                                                                                                        "good_num",
                                                                                                        "remark",
                                                                                                        "good_type_id")
        current_page = request.GET.get('page')  # 当前页
        paginator = Paginator(goods_list, 8)  # 每页展示8条数据
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)
        print(post.object_list)
        return render(request, "Store/goodsManage.html", {"post": post})
    else:
        pass


def addgood(request):
    """
    新增商品
    :param request:
    :return:
    """
    if request.method == "GET":
        addgoodform = GoodForm()
        return render(request, "Store/addGoods.html", {"form": addgoodform})
    else:
        addgoodform = GoodForm(data=request.POST, files=request.FILES)
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        addgoodform.set_store_id(store_id)
        if addgoodform.is_valid():  # 表单验证

            good_type = addgoodform.cleaned_data.get("good_type")
            good_name = addgoodform.cleaned_data.get("good_name")
            good_pic = addgoodform.cleaned_data.get("good_pic")
            price = addgoodform.cleaned_data.get("price")
            discount = addgoodform.cleaned_data.get("discount")
            good_num = addgoodform.cleaned_data.get("good_num")
            remark = addgoodform.cleaned_data.get("remark")
            Goods.objects.create(good_store_id=store_id, good_name=good_name, good_pic=good_pic, price=price,
                                 discount=discount,
                                 good_num=good_num, remark=remark, good_type_id=good_type)
            return redirect("/store/goodsmanage")
        else:
            return render(request, "Store/addGoods.html", {"form": addgoodform})


def addgoodtype(request):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    if request.method == "GET":
        type_list = GoodType.objects.filter(store_id=store_id, goodtype_status=1).values("goodtype_id", "goodtype_name")
        return render(request, "Store/addGoodType.html", {"type_list": type_list})
    else:
        ret = {'status': True, 'message': None}
        try:
            type_name = request.POST.get("type_name")
            goodtype = GoodType.objects.create(goodtype_name=type_name, store_id=store_id)
        except Exception as e:
            ret["status"] = False
            ret["message"] = str(e)
        ret['goodtype_id'] = goodtype.goodtype_id
    return HttpResponse(json.dumps(ret))


def delgoodtype(request):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    ret = {'status': True, 'message': None}
    goodtype_id=request.POST.get("goodtype_id")
    try:
        GoodType.objects.filter(goodtype_id=goodtype_id,store_id=store_id).update(goodtype_status=0)
    except Exception as e:
        ret["status"] = False
        ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))

def goodtypemanage(request):
    if request.method == "GET":
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        goodtype_list = GoodType.objects.filter(store_id=store_id).values_list("goodtype_id", "goodtype_name",
                                                                               "goodtype_status")
        return render(request, "Store/goodTypeManage.html", {"goodtype_list": goodtype_list})


def updategood(request, good_id):
    """
    修改商品
    :param request:
    :param good_id:
    :return:
    """
    if request.method == "GET":
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        good = Goods.objects.filter(good_store_id=store_id, good_id=good_id).values().first()
        if good:
            # 商品存在
            updateGoodForm = GoodForm()
            good_name = good["good_name"]
            good_pic = good["good_pic"]
            good_type_id = good["good_type_id"]
            price = good["price"]
            discount = good["discount"]
            good_num = good["good_num"]
            remark = good["remark"]
            updateGoodForm.set_value(good_name=good_name, good_type_id=good_type_id, price=price, discount=discount,
                                     good_num=good_num, remark=remark)
            return render(request, "Store/updateGood.html",
                          {"form": updateGoodForm, "good_pic": good_pic, "good_id": good_id})
        else:
            # 此商品不存在
            pass
    else:
        updategoodform = GoodForm(data=request.POST, files=request.FILES)
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        updategoodform.set_store_id(-1)
        # 验证表单数据
        if updategoodform.is_valid():
            good_type = updategoodform.cleaned_data.get("good_type")
            good_name = updategoodform.cleaned_data.get("good_name")
            good_pic = updategoodform.cleaned_data.get("good_pic")
            print(good_pic)
            price = updategoodform.cleaned_data.get("price")
            discount = updategoodform.cleaned_data.get("discount")
            print(discount)
            good_num = updategoodform.cleaned_data.get("good_num")
            remark = updategoodform.cleaned_data.get("remark")
            good = Goods.objects.filter(good_id=good_id, good_store_id=store_id)
            if good:
                # 商品存在
                good.update(good_store_id=store_id, good_name=good_name, price=price,
                            discount=discount,
                            good_num=good_num, remark=remark, good_type_id=good_type)
                if good_pic:
                    # 若图片修改
                    good = good.first()
                    good.good_pic = good_pic
                    good.save()
                return redirect("/store/goodsmanage")
            else:
                # 商品不存在
                return render(request, "Store/updateGood.html", {"form": updategoodform, "msg": "不存在此商品"})
        else:
            return render(request, "Store/updateGood.html", {"form": updategoodform})


def delgood(request, good_id):
    """
    删除商品
    :param request:
    :param good_id:
    :return:
    """
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    good = Goods.objects.filter(good_id=good_id, good_store_id=store_id)
    if good:
        good.update(good_status=0)
        return redirect("/store/goodsmanage")
    else:
        pass


def searchgood(request):
    """
    查找商品
    :param request:
    :param page:
    :return:
    """
    if request.method == "GET":
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        good_name = request.GET.get("good_name")
        print(good_name)
        goods_list = Goods.objects.filter(good_store_id=store_id, good_status__gte=1,
                                          good_name__contains=good_name).values_list("good_id", "good_pic", "good_name",
                                                                                     "price", "discount", "good_num",
                                                                                     "remark", "good_type_id")
        current_page = request.GET.get("page")
        paginator = Paginator(goods_list, 8)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)
        print(goods_list)
        return render(request, "Store/goodsManage.html", {"post": post, "search_val": good_name})


def update_good_num(request):
    ret = {'status': True, 'message': None}
    try:
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        num_count = request.POST.get("num_count")
        good_id = request.POST.get("good_id")
        Goods.objects.filter(good_store_id=store_id, good_id=good_id).update(good_num=num_count)
    except Exception as e:
        ret["status"] = False
        ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))


def orderhall(request):
    if request.method == "GET":
        getneworder=False
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]

        order_list = Orders.objects.filter(Q(order_status__gt=0) & Q(order_status__lt=5),
                                           order_store_id=store_id).values("order_id", "total_price", "create_date",
                                                                           "order_status")
        order_detail_list = Order_details.objects.filter(Q(order__order_status__gt=0) & Q(order__order_status__lt=6),
                                                         order__order_store_id=store_id).values("order_id", "good_id",
                                                                                                "good__good_name",
                                                                                                "number")
        new_order_count = Orders.objects.filter(order_status=1, order_store_id=store_id).count()
        order_count = request.session.get("order_count")
        if order_count:
            if new_order_count>order_count:
                getneworder= True
                request.session['order_count']=new_order_count
        else:
            request.session['order_count'] = new_order_count

        for i in order_detail_list:
            for order in order_list:
                if i['order_id'] == order['order_id']:
                    order.get('order_details', order.setdefault('order_details', [])).append(i)
                    order['order_nums'] = i['number'] + order.get('order_nums', 0)
        current_page = request.GET.get('page')
        paginator = Paginator(order_list, 10)
        try:
            post = paginator.page(current_page)
        except PageNotAnInteger or EmptyPage as e:
            print(e)
            post = paginator.page(1)

        return render(request, "Store/OrderHall.html", {"post": post, "new_order_count": new_order_count,"getneworder":getneworder})


def update_order_status(request):
    """
    ajax修改订单状态
    默认为1,(0,订单删除or取消)(1,商家未接单)(2,商家已接单)(3,骑手已接单)(4,骑手取到商品)(5,骑手已送达)
    :param request:
    :return:
    """
    ret = {'status': True, 'message': None}
    try:
        store_info = request.session.get("store_info")
        store_id = store_info["store_id"]
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        Orders.objects.filter(order_id=order_id, order_store_id=store_id).update(order_status=status)
        print(order_id, status)
    except Exception as e:
        ret["status"] = False
        ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))


def ordermanage(request):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    order_list = Orders.objects.filter(order_store_id=store_id, order_status__gte=1).values("order_id", "total_price",
                                                                                            "create_date",
                                                                                            "finish_time",
                                                                                            "order_status")
    all_count = Orders.objects.filter(order_store_id=store_id, order_status__gte=1).count()
    print(all_count)
    page_info = PageInfo(request.GET.get("page"), all_count, 10, '/store/ordermanage', "")
    order_list = order_list[page_info.start():page_info.end()]
    return render(request, "Store/OrderManage.html", {"order_list": order_list, "page_info": page_info})


def updatepwd(request):
    ret = {'status': True, 'message': None}
    oldpwd = request.POST.get("oldpwd")
    newpwd = request.POST.get("newpwd")
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    store_pwd = store_info["pwd"]
    if store_pwd == oldpwd:
        try:
            Stores.objects.filter(store_id=store_id).update(pwd=newpwd)
            store_info["pwd"] = newpwd
            request.session["store_info"] = store_info
            ret["message"] = "修改成功"
        except Exception as e:
            ret["status"] = False
            ret["message"] = "修改失败"
    else:
        ret["status"] = False
        ret["message"] = "原密码错误"
    return HttpResponse(json.dumps(ret))


def orderdetail(request, order_id):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    order = Orders.objects.filter(order_id=order_id, order_store_id=store_id).values("order_id", "total_price",
                                                                                     "order_status", "order_address_id")
    if order:
        detail_list = Order_details.objects.filter(order_id=order_id).values("good_id", "good__good_name", "number")
        address = Address.objects.filter(address_id=order[0]['order_address_id']).values().first()
        print(address)
        return render(request, "Store/OrderDetails.html",
                      {"detail_list": detail_list, "order": order[0], "address": address})
    else:
        return HttpResponse("404 Not Found")


def searchorder(request):
    type = request.GET.get("type")
    if type == "1":
        # 根据时间查找
        starttime = request.GET.get("starttime")
        endtime = request.GET.get("endtime")
        order_list = Orders.objects.filter(create_date__range=(starttime, endtime)).values("order_id", "total_price",
                                                                                           "create_date",
                                                                                           "finish_time",
                                                                                           "order_status")
        all_count = Orders.objects.filter(create_date__range=(starttime, endtime)).count()
        page_info = PageInfo(request.GET.get("page"), all_count, 10,
                             'store/searchorder/?type=' + type + '&starttime=' + starttime + '&endtime=' + endtime)

        print(order_list)
    else:
        search_id = request.GET.get("search_id")
        order_list = Orders.objects.filter(order_id__contains=search_id).values("order_id", "total_price",
                                                                                "create_date",
                                                                                "finish_time",
                                                                                "order_status")
        all_count = Orders.objects.filter(order_id__contains=search_id).count()
        page_info = PageInfo(request.GET.get("page"), all_count, 10, '/store/searchorder/',
                             '&type=' + type + '&search_id=' + search_id)
    order_list = order_list[page_info.start():page_info.end()]
    return render(request, "Store/OrderManage.html", {"order_list": order_list, "page_info": page_info})


def earnmanage(request):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    cur = datetime.datetime.now()
    print(cur)
    # 当天营业额
    today_total_price = Orders.objects.filter(order_store_id=store_id, create_date__day=cur.day).aggregate(
        price=Sum("total_price"), num=Count("total_price"))
    print(today_total_price)
    # 作日营业额
    yesterday = cur - datetime.timedelta(days=1)
    yesterday_total_price = Orders.objects.filter(order_store_id=store_id, create_date__day=yesterday.day).aggregate(
        price=Sum("total_price"), num=Count("total_price"))
    curmonth_total_price = Orders.objects.filter(order_store_id=store_id, create_date__month=cur.month).aggregate(
        price=Sum("total_price"), num=Count("total_price"))
    data_list = Orders.objects.filter(order_store_id=store_id, create_date__year=cur.year).values(
        "create_date__month").annotate(total_orders=Count("order_id"), total_price=Sum("total_price")).order_by(
        "create_date__month")
    columns = []
    orders_list = []
    total_price_list = []
    for data in data_list:
        columns.append(str(data.get("create_date__month")) + "月")
        orders_list.append(data.get('total_orders'))
        total_price_list.append(data.get('total_price'))
    bar = (
        Bar()
            .add_xaxis(columns)
            .add_yaxis('订单数', yaxis_data=orders_list)
            .add_yaxis('销售总额', yaxis_data=total_price_list)
            .set_global_opts(title_opts=opts.TitleOpts(title=str(cur.year) + '年销售统计', subtitle="订单（单位：张）\r\n销售（单位：元）"))
    )
    barchart = bar.render_embed()
    return render(request, "Store/EarnManage.html",
                  {"today": today_total_price, "yesterday": yesterday_total_price, "curmonth": curmonth_total_price,
                   "barchart": barchart})


def echart(request):
    searchtime = request.GET.get("searchtime")
    searchtime = searchtime.split("-")
    print(searchtime)
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    data_list = Orders.objects.filter(order_store_id=store_id, create_date__year=searchtime[0],
                                      create_date__month=searchtime[1]).values("create_date__day").annotate(
        total_orders=Count("order_id"), total_price=Sum("total_price")).order_by("create_date__day")
    if data_list:
        columns = []
        orders_list = []
        total_price_list = []
        for data in data_list:
            columns.append(str(data.get("create_date__day")) + "号")
            orders_list.append(data.get('total_orders'))
            total_price_list.append(data.get('total_price'))
        bar = (
            Bar()
                .add_xaxis(columns)
                .add_yaxis('订单数', yaxis_data=orders_list)
                .add_yaxis('销售总额', yaxis_data=total_price_list)
                .set_global_opts(
                title_opts=opts.TitleOpts(title=str(searchtime[1]) + '月销售统计', subtitle="订单（单位：张）\r\n销售（单位：元）"))
        )
        return render(request, "Store/echartDetails.html", {"echart": bar.render_embed()})
    else:
        return render(request, "Store/echartDetails.html", {"echart": "本月暂无记录"})


def updateinfo(request):
    store_info = request.session.get("store_info")
    store_id = store_info["store_id"]
    if request.method == "GET":
        store = Stores.objects.filter(store_id=store_id).values("account", "store_name", "store_avatar", "store_tel",
                                                                "address",
                                                                "open_time", "close_time", "remark").first()

        # print(store)
        update_store_info = UpdateStoreForm(initial=store)
        return render(request, "Store/UpdateStoreInfo.html", {"store": store, "form": update_store_info})
    else:
        form = UpdateStoreForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            store_avatar = form.cleaned_data.get("store_avatar")
            print(store_avatar, type(store_avatar))
            store_name = form.cleaned_data.get("store_name")
            store_tel = form.cleaned_data.get("store_tel")
            address = form.cleaned_data.get("address")
            open_time = form.cleaned_data.get("open_time")
            close_time = form.cleaned_data.get("close_time")
            remark = form.cleaned_data.get("remark")
            store = Stores.objects.filter(store_id=store_id)
            store.update(store_name=store_name, store_tel=store_tel, address=address, open_time=open_time,
                         close_time=close_time, remark=remark)
            store = store.first()
            store.store_avatar = store_avatar
            store.save()
            print(request.POST)
            return redirect("/store/orderhall/")
        else:
            print(form.errors)

