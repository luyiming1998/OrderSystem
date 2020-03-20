from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
from .models import Goods, GoodType


class GoodForm(Form):
    good_pic = fields.ImageField(
        label="商品图片",
        required=False,
        widget=widgets.FileInput()
    )
    good_name = fields.CharField(
        label="名称",
        required=True,
        max_length=10,
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            'required': '商品名称不能为空',
            'max_length': '商品名称长度不能超过10',
        }
    )
    price = fields.FloatField(
        label="单价",
        required=True,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
    )
    discount = fields.FloatField(
        label="折扣",
        required=False,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
    )
    good_num = fields.IntegerField(
        label="库存",
        required=True,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
    )
    remark = fields.CharField(
        label="备注",
        required=False,
        widget=widgets.Textarea(attrs={"class": "form-control"})
    )
    good_type = fields.ChoiceField(
        # choices=GoodType.objects.filter(store_id=1, goodtype_status=1).values_list("goodtype_id", "goodtype_name"),
        label="商品类型",
        initial=1,
        widget=widgets.Select(attrs={"class": "form-control", "style": "width:150px;display:inline"})
    )

    def __init__(self, *args, **kwargs):
        super(GoodForm, self).__init__(*args, **kwargs)  # 调用父类的__init__
        self.fields['good_type'].choices = GoodType.objects.filter(store_id=1, goodtype_status=1).values_list(
            "goodtype_id", "goodtype_name")

    def set_store_id(self, store_id):
        self.store_id = store_id

    def clean_discount(self):
        val = self.cleaned_data.get("discount")
        if val:
            if 1 >= val > 0:
                return val
            else:
                raise ValidationError("优惠打折须在0-1之间")
        else:
            return val

    def clean_price(self):
        val = self.cleaned_data.get("price")
        if 0 <= val <= 9999:
            return val
        else:
            raise ValidationError("商品价格须在0-999之间")

    def clean_good_name(self):
        val = self.cleaned_data.get("good_name")
        store_id = self.store_id
        ret = Goods.objects.filter(good_name=val, good_store_id=store_id)
        if not ret:
            return val
        else:
            raise ValidationError("本店已存在同名商品")

    def set_value(self, good_type_id, good_name, price, discount, good_num, remark, ):
        self.initial['good_type'] = good_type_id
        self.fields['good_name'].widget.attrs.update({'value': good_name if good_name is not None else ""})
        self.fields['price'].widget.attrs.update({'value': price if price is not None else ""})
        self.fields['discount'].widget.attrs.update({'value': discount if discount is not None else ""})
        self.fields['good_num'].widget.attrs.update({'value': good_num if good_num is not None else ""})
        self.initial['remark'] = remark


class UpdateStoreForm(Form):
    store_id = fields.CharField(
        required=False
    )
    store_name = fields.CharField(
        label="商家名称",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    store_avatar = fields.ImageField(
        label="头像",
        required=False,
        widget=widgets.FileInput()
    )
    store_tel = fields.CharField(
        label="联系方式",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    address = fields.CharField(
        label="地址",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    open_time = fields.TimeField(
        label="开店时间",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    close_time = fields.TimeField(
        label="关店时间",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    remark = fields.CharField(
        label="商家介绍",
        widget=widgets.Textarea(attrs={"class": "form-control"})
    )
