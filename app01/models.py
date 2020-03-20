from django.db import models


# Create your models here.

class Users(models.Model):
    """
    用户
    """
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    account = models.CharField(max_length=20, verbose_name="账号")
    pwd = models.CharField(max_length=16, verbose_name="密码")
    user_name = models.CharField(max_length=10, verbose_name="用户名")
    user_tel = models.CharField(max_length=11, verbose_name="手机号")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="用户创建时间")
    user_avatar = models.ImageField(upload_to='user_avatar/', verbose_name="用户头像", default="userDefault.png")
    user_status = models.IntegerField(default=1, verbose_name="用户状态")  # 默认为1,(1,激活)(0,注销)

    class Meta:
        unique_together = ("account", "user_tel")


class Riders(models.Model):
    """
    骑手
    """
    rider_id = models.AutoField(primary_key=True, verbose_name="骑手ID")
    account = models.CharField(max_length=20, verbose_name="骑手账号")
    pwd = models.CharField(max_length=16, verbose_name="密码")
    rider_name = models.CharField(max_length=5, verbose_name="骑手真实姓名")
    identity_card = models.CharField(max_length=18, verbose_name="身份证")
    identity_card_front = models.ImageField(upload_to='riders_identity_card/', verbose_name="骑手身份证正面")
    identity_card_back = models.ImageField(upload_to='riders_identity_card/', verbose_name="骑手身份证反面")
    rider_tel = models.CharField(max_length=11, verbose_name="手机号")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="用户创建时间")
    rider_status = models.IntegerField(default=1, verbose_name="骑手状态")  # 默认为1,(0,骑手已离职或未激活)(1,骑手休息不接单)(2,骑手上班开始接单)
    earnmoney = models.FloatField(verbose_name="收益", default=0.00)

    class Meta:
        unique_together = ("account", "rider_tel")


class Stores(models.Model):
    """商家"""
    store_id = models.AutoField(primary_key=True, verbose_name="商家ID")
    account = models.CharField(max_length=20, verbose_name="商家账号")
    pwd = models.CharField(max_length=16, verbose_name="密码")
    real_name = models.CharField(max_length=5, verbose_name="商家真实姓名")
    identity_card = models.CharField(max_length=18, verbose_name="身份证",null=True)
    identity_card_front = models.ImageField(upload_to='stores_identity_card/', verbose_name="商家身份证正面",null=True)
    identity_card_back = models.ImageField(upload_to='stores_identity_card/', verbose_name="商家身份证反面",null=True)
    store_name = models.CharField(max_length=20, verbose_name="商家名称")
    store_avatar = models.ImageField(upload_to='store_avatar/', verbose_name="商家头像", default="storeDefault.png")
    store_tel = models.CharField(max_length=11, verbose_name="手机号")
    address = models.CharField(max_length=20, verbose_name="商家地址")
    open_time = models.TimeField(verbose_name="开店时间")
    close_time = models.TimeField(verbose_name="关店时间")
    remark = models.CharField(max_length=200, null=True, verbose_name="商家介绍")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="用户创建时间")
    store_status = models.IntegerField(default=0, verbose_name="商家状态")  # 默认为0，(0,未认证成功),(1,开始营业)(2,未营业)

    class Meta:
        unique_together = ("account", "store_tel")


class Goods(models.Model):
    """商家商品"""
    good_id = models.AutoField(primary_key=True, verbose_name="商品ID")
    good_name=models.CharField(max_length=15,verbose_name="商品名称")
    good_store = models.ForeignKey("Stores", on_delete=models.CASCADE, verbose_name="商家")
    good_type = models.ForeignKey("GoodType", null=True, on_delete=models.CASCADE, verbose_name="商品类型")
    good_pic = models.ImageField(upload_to='good_pic/%Y/%m', verbose_name="商品图片", default="good_pic/default.png")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="商品单价", )
    discount = models.FloatField(default=1.00, verbose_name="折扣",null=True,blank=True)
    good_num = models.IntegerField(default=0, verbose_name="商品库存")
    remark = models.CharField(max_length=200, null=True, verbose_name="商品介绍")
    good_status=models.IntegerField(default=1, verbose_name="商品状态")  # 默认为1(0,已删除)(1,激活)(2,下架)


class GoodType(models.Model):
    goodtype_id = models.AutoField(primary_key=True, verbose_name="商品类型ID")
    goodtype_name = models.CharField(max_length=10, verbose_name="商品类型名称")
    store = models.ForeignKey("Stores", on_delete=models.CASCADE, verbose_name="商店id")
    goodtype_status = models.IntegerField(default=1, verbose_name="商品类型状态")  # 默认为1(0,已删除)(1,激活)


class Orders(models.Model):
    """订单"""
    order_id = models.AutoField(primary_key=True, verbose_name="订单ID")
    order_user = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="用户id")
    order_rider = models.ForeignKey("Riders", on_delete=models.CASCADE, verbose_name="骑手id",null=True)
    order_store = models.ForeignKey("Stores", on_delete=models.CASCADE, verbose_name="商家id")
    order_address = models.ForeignKey("Address", on_delete=models.CASCADE, verbose_name="送餐地址id")
    total_price = models.FloatField(verbose_name="总价")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="订单创建时间")
    finish_time = models.DateTimeField(verbose_name="完成时间", null=True)
    order_status = models.IntegerField(default=1, verbose_name="订单状态")
    # 默认为1,(0,订单删除or取消)(1,商家未接单)(2,商家已接单)(3,骑手已接单)(4,骑手取到商品)(5,骑手已送达)
    order_detail = models.ManyToManyField("Goods", through="Order_details")
    comment = models.OneToOneField("Comment", null=True, on_delete=models.CASCADE, verbose_name="评论id")

class Order_details(models.Model):
    """订单详情"""
    order_detail_id = models.AutoField(primary_key=True, verbose_name="订单详情ID")
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, verbose_name="订单")
    good = models.ForeignKey("Goods", on_delete=models.CASCADE, verbose_name="商品id")
    number = models.IntegerField(default=1, verbose_name="数量")
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="折扣后单价")


class Address(models.Model):
    """用户地址"""
    address_id = models.AutoField(primary_key=True, verbose_name="地址id")
    location = models.CharField(max_length=20, verbose_name="地址")
    address_user = models.ForeignKey("Users", on_delete=models.CASCADE, verbose_name="用户")
    address_name = models.CharField(max_length=10, verbose_name="姓名")
    address_tel = models.CharField(max_length=11, verbose_name="手机号")
    sex = models.IntegerField(default=1, verbose_name="性别")  # 默认为1,(1,男)(2,女)
    address_status = models.IntegerField(default=1, verbose_name="地址状态")  # 默认未1(0,删除)(1,未删除)


class Comment(models.Model):
    """用户评价"""
    comment_id = models.AutoField(primary_key=True, verbose_name="评价ID")
    comment_content = models.CharField(max_length=300, verbose_name="评价内容")
    level=models.IntegerField(default=1,verbose_name="星级评分")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    comment_status = models.IntegerField(default=1, verbose_name="评论状态")  # 默认为1,(0,已删除)(1,已评论)(2,商家已读)
