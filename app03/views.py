from django.shortcuts import render,redirect
from .form import *
from app01.models import *
# Create your views here.
def storeregister(request):
    if request.method=="GET":
        regform=StoreRegister()
        return render(request,"Base/StoreRegister.html",{"form":regform})
    else:
        regform=StoreRegister(data=request.POST,files=request.FILES)
        if regform.is_valid():
            account = regform.cleaned_data.get("account")
            pwd = regform.cleaned_data.get('pwd')
            real_name=regform.cleaned_data.get("real_name")
            identity_card=regform.cleaned_data.get("identity_card")
            store_name = regform.cleaned_data.get('store_name')
            store_tel = regform.cleaned_data.get('store_tel')
            address = regform.cleaned_data.get('address')
            open_time = regform.cleaned_data.get('open_time')
            close_time = regform.cleaned_data.get('close_time')
            remark = regform.cleaned_data.get('remark')
            store_avatar=regform.cleaned_data.get("store_avatar")
            Stores.objects.create(account=account,pwd=pwd,store_avatar=store_avatar,real_name=real_name,identity_card=identity_card,store_name=store_name,store_tel=store_tel,address=address,store_status=1,open_time=open_time,close_time=close_time,remark=remark)
            return redirect("/login/")
        else:
            return render(request, "Base/StoreRegister.html", {"form": regform})


def userregister(request):
    if request.method=="GET":
        regform=UserRegister()
        return render(request,"Base/UserRegister.html",{"form":regform})
    else:
        regform=UserRegister(data=request.POST,files=request.FILES)
        if regform.is_valid():
            account = regform.cleaned_data.get("account")
            pwd = regform.cleaned_data.get('pwd')
            user_name = regform.cleaned_data.get('user_name')
            user_tel = regform.cleaned_data.get('user_tel')
            user_avatar=regform.cleaned_data.get("user_avatar")
            Users.objects.create(account=account,pwd=pwd,user_avatar=user_avatar,user_name=user_name,user_tel=user_tel,user_status=1)
            return redirect("/login/")
        else:
            return render(request, "Base/UserRegister.html", {"form": regform})

def riderregister(request):
    if request.method=="GET":
        regform=RiderRegister()
        return render(request,"Base/RiderRegister.html",{"form":regform})
    else:
        regform=RiderRegister(request.POST)
        if regform.is_valid():
            account = regform.cleaned_data.get("account")
            pwd = regform.cleaned_data.get('pwd')
            rider_name = regform.cleaned_data.get('rider_name')
            rider_tel = regform.cleaned_data.get('rider_tel')
            identity_card=regform.cleaned_data.get('identity_card')
            Riders.objects.create(account=account,pwd=pwd,rider_name=rider_name,rider_tel=rider_tel,identity_card=identity_card,rider_status=1)
            return redirect("/login/")
        else:
            return render(request, "Base/RiderRegister.html", {"form": regform})
def login(request):
    if request.method=="GET":
        return render(request,"Base/login.html")
    else:
        login_type=request.POST.get("type")
        account=request.POST.get("account")
        pwd=request.POST.get("pwd")
        print(account,pwd)
        if login_type=="1":
            user=Users.objects.filter(account=account,pwd=pwd,user_status=1).values("user_id","account","pwd","user_avatar","user_name").first()
            print(user)
            if user:
                request.session["user_info"]=user
                return redirect('/user/goodsmanage/')
            else:
                return render(request, "Base/login.html")
        elif login_type=="2":
            store_info = Stores.objects.filter(account=account, pwd=pwd, store_status__gte=1).values("store_id",
                                                                                                     "store_name",
                                                                                                     "pwd",
                                                                                                     "store_avatar").first()
            if store_info:
                request.session["store_info"] = store_info
                return redirect("/store/orderhall/")
            else:
                return render(request, "Base/login.html")

        elif login_type=="3":
            rider=Riders.objects.filter(account=account,pwd=pwd,rider_status=1).values("rider_id","rider_name","account","pwd")
            if rider:
                request.session["rider_info"] = rider
                return redirect("/rider/OrderHall/")
            else:
                return render(request, "Base/login.html")
        else:
            return render(request, "Base/login.html")

