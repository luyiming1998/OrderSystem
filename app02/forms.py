from django.forms import Form
from django import forms
from  django.forms import fields
class UpdateForm(Form):
    user_id = fields.IntegerField()
    account = fields.CharField(
        max_length=20,
        required=True,
        error_messages={
            'required':'用户名不能为空',
            'max_length':'太长了',
        }
    )
    pwd = fields.CharField(
        max_length=16,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '太长了',
        }
    )
    user_name = fields.CharField(
        max_length=10,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '太长了',
        }
    )
    user_tel = fields.CharField(
        max_length=11,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '太长了',
        }
    )

class UserOrder(forms.Form):
    total_price = forms.FloatField(error_messages={'required':'用户名为空'})
    store_id = forms.IntegerField(error_messages={'required':'用户名为空'})


class AddressAdd(forms.Form):
    location = forms.CharField(max_length=20,error_messages={'required':'用户名为空'})
    user_name = forms.CharField(max_length=10,error_messages={'required':'用户名为空'})
    address_tel = forms.CharField(max_length=11,error_messages={'required':'用户名为空'})
    sex =forms.IntegerField(error_messages={'required':'用户名为空'})
class EditAddress(forms.Form):
    address_id = forms.IntegerField()
    location = forms.CharField(max_length=20,error_messages={'required':'用户名为空'})
    user_name = forms.CharField(max_length=10,error_messages={'required':'用户名为空'})
    address_tel = forms.CharField(max_length=11,error_messages={'required':'用户名为空'})
    sex =forms.IntegerField(error_messages={'required':'用户名为空'})





