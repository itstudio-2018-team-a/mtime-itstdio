from django import forms

from . import models


import re


class RegisterForm(forms.ModelForm):

    class Meta:
        model = models.User

        fields = {'username', 'password', 'nickname', 'head_image', 'email', 'active'}

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6 or len(username) > 16:
            raise forms.ValidationError('用户名长度为6 ~ 16位')
        if re.search(r'\W', username):
            raise forms.ValidationError('用户名不合法')
        if not (re.search(r'\d', username) and re.search(r'\w', username)):
            raise forms.ValidationError('用户名必须包含数字、字母或下划线')

        user = models.User.objects.filter(username=username)
        if user:
            raise forms.ValidationError('此用户名存在')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6 or len(password) > 16:
            raise forms.ValidationError('密码长度为6 ~ 16位')

        for i in range(len(password)):
            if ord(password[i]) < 33 or ord(password[i]) > 126:
                raise forms.ValidationError('密码格式错误')

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.search(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise forms.ValidationError('邮箱格式错误')
        if models.User.objects.filter(email=email):
            raise forms.ValidationError('邮箱已被注册')

        return email


class VerificationCodeForm(forms.ModelForm):

    class Meta:
        model = models.VerificationCode
        fields = ('email', 'code')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.search(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise forms.ValidationError('邮箱格式错误')
        if models.User.objects.filter(email=email):
            raise forms.ValidationError('邮箱已被注册')

        email_code = models.VerificationCode.objects.filter(email=email)
        if email_code:
            email_code.delete()

        return email

    def clean_code(self):
        code = self.cleaned_data['code']

        # ......

        return code






