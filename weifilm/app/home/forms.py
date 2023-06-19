#coding:utf8
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SelectField,SelectMultipleField,SubmitField,TextAreaField,TextField,PasswordField,FileField
from wtforms.validators import DataRequired,ValidationError,EqualTo,Email,Regexp
from app.models import User

class RegisterForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称!")
        ],
        description="昵称",
        render_kw={
            "class":"form-control input-lg" ,
            "placeholder":"请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱!"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码!"),
            Regexp('1[345789]\\d{9}',message='手机号码格式不正确')
        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！",
        }
    )
    pwd = PasswordField(
        label = "密码",
        validators=[
            DataRequired("请输入密码！"),
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",
            # "required": "required"
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd',message='两次密码不一致！')
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )
    def validate_account(self,field):
        account = field.data
        admin = User.query.filter_by(name=account).count()
        if admin == 1:
            raise ValidationError("昵称已经存在！")

    def validate_email(self,field):
        account = field.data
        admin = User.query.filter_by(email=account).count()
        if admin == 1:
            raise ValidationError("邮箱已经被注册！")
    def validate_phone(self,field):
        account = field.data
        admin = User.query.filter_by(phone=account).count()
        if admin == 1:
            raise ValidationError("手机号已经被注册！")

class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号!")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # "required":"required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = User.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在!")

class UserdetailForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称!")
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱!"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码!"),
            Regexp('1[345789]\\d{9}', message='手机号码格式不正确')
        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！",
        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像!"),
        ],
        description="头像",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介!"),
        ],
        description="简介",
        render_kw={
            "class": "form-control input-lg",
            'rows':10
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-success",
        }
    )
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
            # "required": "required"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
        }
    )
    def validate_old_pwd(self,field):
        from flask import session
        pwd = field.data
        name = session['user']
        user = User.query.filter_by(
            name=name
        ).first()
        if not user.check_pwd(pwd):
            raise ValidationError("旧密码错误！")

class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请输入评论内容！")
        ],
        description="内容",
        render_kw={
            "id":"btn-sub",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "class": "btn btn-success",
            "id":"btn-sub"
        }
    )
