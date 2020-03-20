from django.forms import Form, widgets, fields


class StoreRegister(Form):
    account = fields.CharField(
        label="账号",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    check_pwd = fields.CharField(
        label="确认密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    real_name = fields.CharField(
        label="真实姓名",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    identity_card = fields.CharField(
        label="身份证号",
        widget=widgets.TextInput(attrs={"class": "form-control"})
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


class UserRegister(Form):
    account = fields.CharField(
        label="账号",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    check_pwd = fields.CharField(
        label="确认密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    user_name = fields.CharField(
        label="昵称",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    user_avatar = fields.ImageField(
        label="头像",
        required=False,
        widget=widgets.FileInput()
    )
    user_tel = fields.CharField(
        label="联系方式",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )


class RiderRegister(Form):
    account = fields.CharField(
        label="账号",
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    check_pwd = fields.CharField(
        label="确认密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )
    rider_name = fields.CharField(
        max_length=5,
        label="骑手真实姓名",
        required=True,
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            'required': '姓名不能为空',
            'max_length': '长度不能超过5',
        }
    )
    identity_card = fields.CharField(
        max_length=18,
        label="身份证",
        required=True,
        widget=widgets.TextInput(attrs={"class": "form-control"}),
    )
    rider_tel = fields.CharField(
        max_length=11,
        label="手机号",
        required=True,
        widget=widgets.TextInput(attrs={"class": "form-control"}),
    )